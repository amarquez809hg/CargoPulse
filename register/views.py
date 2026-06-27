from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods

from .availability import POST_VISIBILITY_DAYS, visible_posts
from .decorators import get_profile, role_required
from .models import PortOfEntry, TruckAvailability, TruckingCompany, UserProfile

CARRIER_PROFILE_FIELDS = (
    "username",
    "email",
    "password",
    "password2",
    "company_name",
    "company_address",
    "hq_city",
    "primary_port_of_entry",
    "popular_destinations",
    "whatsapp_number",
)

AVAILABILITY_FIELDS = (
    "lane_type",
    "port_of_entry",
    "location_address",
    "current_city",
    "destination_city",
    "equipment_type",
    "trailer_length_ft",
    "load_type",
    "weight_lbs",
    "min_rate_per_mile",
    "reference_id",
    "equipment_notes",
)

VALID_PORTS = {c.value for c in PortOfEntry}
VALID_LANE_TYPES = {c.value for c in TruckAvailability.LaneType}
VALID_EQUIPMENT = {c.value for c in TruckAvailability.EquipmentType}
VALID_LOAD_TYPES = {c.value for c in TruckAvailability.LoadType}


def _clear_messages(request):
    storage = messages.get_messages(request)
    storage.used = True


def _build_whatsapp(code, number):
    code = (code or "+52").strip()
    number = (number or "").strip().replace(" ", "").replace("-", "")
    if number.startswith("+"):
        return number
    if number.startswith("00"):
        return "+" + number[2:]
    return f"{code}{number}"


def _parse_optional_int(value):
    if not value:
        return None
    return int(value)


def _parse_optional_decimal(value):
    if not value:
        return None
    return Decimal(value)


def _redirect_for_user(user):
    profile = get_profile(user)
    if not profile:
        if user.is_staff:
            return redirect("/admin/")
        return redirect("home")
    if profile.role == UserProfile.ROLE_CARRIER:
        return redirect("carrier_dashboard")
    return redirect("broker_board")


def home(request):
    if request.user.is_authenticated:
        return _redirect_for_user(request.user)
    return render(request, "register/home.html")


@require_http_methods(["GET", "POST"])
def auth_login(request):
    if request.user.is_authenticated:
        return _redirect_for_user(request.user)

    role_hint = request.GET.get("role", "")
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            _clear_messages(request)
            messages.success(
                request,
                _("Welcome back, %(username)s.") % {"username": user.username},
            )
            return _redirect_for_user(user)
        return render(
            request,
            "register/auth/login.html",
            {"role_hint": role_hint, "error": _("Invalid username or password.")},
        )

    return render(request, "register/auth/login.html", {"role_hint": role_hint})


def auth_logout(request):
    logout(request)
    return redirect("home")


@require_http_methods(["GET", "POST"])
def carrier_signup(request):
    if request.user.is_authenticated:
        return _redirect_for_user(request.user)

    f = {"whatsapp_code": "+52", "whatsapp_number": "", "ctpat_certified": False, "b1_drivers": False}
    ctx = {
        "f": f,
        "port_of_entry_choices": PortOfEntry.choices,
    }

    if request.method == "POST":
        f = {k: (request.POST.get(k) or "").strip() for k in CARRIER_PROFILE_FIELDS}
        f["whatsapp_code"] = (request.POST.get("whatsapp_code") or "+52").strip()
        f["ctpat_certified"] = request.POST.get("ctpat_certified") == "1"
        f["b1_drivers"] = request.POST.get("b1_drivers") == "1"
        ctx["f"] = f

        if f["password"] != f["password2"]:
            ctx["error"] = _("Passwords do not match.")
            return render(request, "register/auth/signup_carrier.html", ctx)
        if User.objects.filter(username=f["username"]).exists():
            ctx["error"] = _("Username already taken.")
            return render(request, "register/auth/signup_carrier.html", ctx)
        if User.objects.filter(email=f["email"]).exists():
            ctx["error"] = _("Email already registered.")
            return render(request, "register/auth/signup_carrier.html", ctx)
        if f["primary_port_of_entry"] and f["primary_port_of_entry"] not in VALID_PORTS:
            ctx["error"] = _("Select a valid border crossing.")
            return render(request, "register/auth/signup_carrier.html", ctx)

        user = User.objects.create_user(
            username=f["username"],
            email=f["email"],
            password=f["password"],
        )
        UserProfile.objects.create(user=user, role=UserProfile.ROLE_CARRIER)
        TruckingCompany.objects.create(
            user=user,
            company_name=f["company_name"],
            email=f["email"],
            whatsapp=_build_whatsapp(f["whatsapp_code"], f["whatsapp_number"]),
            company_address=f["company_address"],
            hq_city=f["hq_city"],
            primary_port_of_entry=f["primary_port_of_entry"],
            popular_destinations=f["popular_destinations"],
            ctpat_certified=f["ctpat_certified"],
            b1_drivers=f["b1_drivers"],
        )
        login(request, user)
        _clear_messages(request)
        messages.success(request, _("Carrier account created. You can post equipment now."))
        return redirect("carrier_dashboard")

    return render(request, "register/auth/signup_carrier.html", ctx)


@require_http_methods(["GET", "POST"])
def broker_signup(request):
    if request.user.is_authenticated:
        return _redirect_for_user(request.user)

    f = {}
    if request.method == "POST":
        f = {k: (request.POST.get(k) or "").strip() for k in (
            "username", "email", "password", "password2",
            "display_name", "brokerage_name",
        )}

        if f["password"] != f["password2"]:
            return render(request, "register/auth/signup_broker.html", {
                "f": f, "error": _("Passwords do not match."),
            })
        if User.objects.filter(username=f["username"]).exists():
            return render(request, "register/auth/signup_broker.html", {
                "f": f, "error": _("Username already taken."),
            })
        if User.objects.filter(email=f["email"]).exists():
            return render(request, "register/auth/signup_broker.html", {
                "f": f, "error": _("Email already registered."),
            })

        user = User.objects.create_user(
            username=f["username"],
            email=f["email"],
            password=f["password"],
        )
        UserProfile.objects.create(
            user=user,
            role=UserProfile.ROLE_BROKER,
            display_name=f["display_name"],
            brokerage_name=f["brokerage_name"],
        )
        login(request, user)
        _clear_messages(request)
        messages.success(request, _("Broker account created. Browse available trucks."))
        return redirect("broker_board")

    return render(request, "register/auth/signup_broker.html", {"f": f})


@role_required(UserProfile.ROLE_CARRIER)
def carrier_dashboard(request):
    company = get_object_or_404(TruckingCompany, user=request.user)
    posts = visible_posts(company.posts.all())
    return render(request, "register/carrier/dashboard.html", {
        "company": company,
        "posts": posts,
        "post_visibility_days": POST_VISIBILITY_DAYS,
    })


@role_required(UserProfile.ROLE_CARRIER)
@require_http_methods(["GET", "POST"])
def carrier_post_truck(request):
    company = get_object_or_404(TruckingCompany, user=request.user)
    default_port = company.primary_port_of_entry or ""
    f = {
        "port_of_entry": default_port,
        "location_address": company.company_address,
        "trailer_length_ft": "53",
    }
    ctx = {
        "company": company,
        "f": f,
        "post_visibility_days": POST_VISIBILITY_DAYS,
        "lane_type_choices": TruckAvailability.LaneType.choices,
        "port_of_entry_choices": PortOfEntry.choices,
        "equipment_type_choices": TruckAvailability.EquipmentType.choices,
        "load_type_choices": TruckAvailability.LoadType.choices,
    }

    if request.method == "POST":
        f = {k: (request.POST.get(k) or "").strip() for k in AVAILABILITY_FIELDS}
        ctx["f"] = f

        if not f["lane_type"] or not f["current_city"] or not f["destination_city"]:
            ctx["errors"] = _("Type, origin city, and destination city are required.")
            return render(request, "register/carrier/post.html", ctx)

        if f["lane_type"] not in VALID_LANE_TYPES:
            ctx["errors"] = _("Select a valid type.")
            return render(request, "register/carrier/post.html", ctx)

        if f["port_of_entry"] and f["port_of_entry"] not in VALID_PORTS:
            ctx["errors"] = _("Select a valid port of entry.")
            return render(request, "register/carrier/post.html", ctx)

        if f["equipment_type"] not in VALID_EQUIPMENT:
            ctx["errors"] = _("Select a valid equipment type.")
            return render(request, "register/carrier/post.html", ctx)

        if f["load_type"] not in VALID_LOAD_TYPES:
            ctx["errors"] = _("Select a valid load type.")
            return render(request, "register/carrier/post.html", ctx)

        try:
            trailer_length = int(f["trailer_length_ft"] or "53")
            if trailer_length < 1 or trailer_length > 75:
                raise ValueError
            weight_lbs = _parse_optional_int(f["weight_lbs"])
            min_rate = _parse_optional_decimal(f["min_rate_per_mile"])
        except (ValueError, InvalidOperation):
            ctx["errors"] = _("Check trailer length, weight, and rate values.")
            return render(request, "register/carrier/post.html", ctx)

        TruckAvailability.objects.create(
            company=company,
            lane_type=f["lane_type"],
            port_of_entry=f["port_of_entry"],
            location_address=f["location_address"],
            current_city=f["current_city"],
            destination_city=f["destination_city"],
            equipment_type=f["equipment_type"],
            trailer_length_ft=trailer_length,
            load_type=f["load_type"],
            weight_lbs=weight_lbs,
            min_rate_per_mile=min_rate,
            reference_id=f["reference_id"],
            post_status=TruckAvailability.PostStatus.OPEN,
            equipment_notes=f["equipment_notes"],
        )
        messages.success(request, _("Equipment availability posted."))
        return redirect("carrier_dashboard")

    return render(request, "register/carrier/post.html", ctx)


@role_required(UserProfile.ROLE_BROKER)
def broker_board(request):
    trucks = visible_posts(
        TruckAvailability.objects.select_related("company").all()
    ).order_by("-created_at")

    city_filter = (request.GET.get("city") or "").strip()
    lane_type_filter = (request.GET.get("lane_type") or "").strip()
    port_filter = (request.GET.get("port_of_entry") or "").strip()
    equipment_filter = (request.GET.get("equipment_type") or "").strip()

    if city_filter:
        trucks = trucks.filter(
            Q(current_city__icontains=city_filter)
            | Q(destination_city__icontains=city_filter)
            | Q(location_address__icontains=city_filter)
            | Q(company__popular_destinations__icontains=city_filter)
            | Q(company__hq_city__icontains=city_filter)
            | Q(company__company_address__icontains=city_filter)
        )
    if lane_type_filter and lane_type_filter in VALID_LANE_TYPES:
        trucks = trucks.filter(lane_type=lane_type_filter)
    if port_filter and port_filter in VALID_PORTS:
        trucks = trucks.filter(port_of_entry=port_filter)
    if equipment_filter and equipment_filter in VALID_EQUIPMENT:
        trucks = trucks.filter(equipment_type=equipment_filter)

    stats = trucks.aggregate(
        post_count=Count("id"),
        carrier_count=Count("company", distinct=True),
        route_count=Count("destination_city", distinct=True),
    )

    has_filters = any([city_filter, lane_type_filter, port_filter, equipment_filter])

    return render(request, "register/broker/board.html", {
        "trucks": trucks,
        "city_filter": city_filter,
        "lane_type_filter": lane_type_filter,
        "port_filter": port_filter,
        "equipment_filter": equipment_filter,
        "stats": stats,
        "has_filters": has_filters,
        "post_visibility_days": POST_VISIBILITY_DAYS,
        "lane_type_choices": TruckAvailability.LaneType.choices,
        "port_of_entry_choices": PortOfEntry.choices,
        "equipment_type_choices": TruckAvailability.EquipmentType.choices,
    })
