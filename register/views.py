from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods

from .decorators import get_profile, role_required
from .models import TruckAvailability, TruckingCompany, UserProfile

AVAILABILITY_FIELDS = (
    "lane_type",
    "port_of_entry",
    "current_city",
    "current_state",
    "destination_city",
    "destination_state",
    "equipment_notes",
)

VALID_PORTS = {c.value for c in TruckAvailability.PortOfEntry}
VALID_LANE_TYPES = {c.value for c in TruckAvailability.LaneType}


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

    f = {"whatsapp_code": "+52", "whatsapp_number": ""}
    if request.method == "POST":
        f = {k: (request.POST.get(k) or "").strip() for k in (
            "username", "email", "password", "password2",
            "company_name", "hq_city", "hq_state", "whatsapp_number",
        )}
        f["whatsapp_code"] = (request.POST.get("whatsapp_code") or "+52").strip()

        if f["password"] != f["password2"]:
            return render(request, "register/auth/signup_carrier.html", {
                "f": f, "error": _("Passwords do not match."),
            })
        if User.objects.filter(username=f["username"]).exists():
            return render(request, "register/auth/signup_carrier.html", {
                "f": f, "error": _("Username already taken."),
            })
        if User.objects.filter(email=f["email"]).exists():
            return render(request, "register/auth/signup_carrier.html", {
                "f": f, "error": _("Email already registered."),
            })

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
            hq_city=f["hq_city"],
            hq_state=f["hq_state"],
        )
        login(request, user)
        _clear_messages(request)
        messages.success(request, _("Carrier account created. You can post equipment now."))
        return redirect("carrier_dashboard")

    return render(request, "register/auth/signup_carrier.html", {"f": f})


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
    posts = company.posts.all()
    return render(request, "register/carrier/dashboard.html", {
        "company": company,
        "posts": posts,
    })


@role_required(UserProfile.ROLE_CARRIER)
@require_http_methods(["GET", "POST"])
def carrier_post_truck(request):
    company = get_object_or_404(TruckingCompany, user=request.user)
    f = {}
    ctx = {
        "company": company,
        "f": f,
        "lane_type_choices": TruckAvailability.LaneType.choices,
        "port_of_entry_choices": TruckAvailability.PortOfEntry.choices,
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

        TruckAvailability.objects.create(
            company=company,
            lane_type=f["lane_type"],
            port_of_entry=f["port_of_entry"],
            current_city=f["current_city"],
            current_state=f["current_state"],
            destination_city=f["destination_city"],
            destination_state=f["destination_state"],
            equipment_notes=f["equipment_notes"],
        )
        messages.success(request, _("Equipment availability posted."))
        return redirect("carrier_dashboard")

    return render(request, "register/carrier/post.html", ctx)


@role_required(UserProfile.ROLE_BROKER)
def broker_board(request):
    trucks = (
        TruckAvailability.objects.select_related("company")
        .all()
        .order_by("-created_at")
    )
    city_filter = (request.GET.get("city") or "").strip()
    if city_filter:
        trucks = trucks.filter(
            Q(current_city__icontains=city_filter)
            | Q(destination_city__icontains=city_filter)
        )
    return render(request, "register/broker/board.html", {
        "trucks": trucks,
        "city_filter": city_filter,
    })
