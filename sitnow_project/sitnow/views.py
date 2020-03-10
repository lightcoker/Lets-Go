from django.shortcuts import render
from sitnow.forms import UserForm, UserProfileForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# Create your views here.


def index(request):
    context_dict = {}
    context_dict["welcome_msg"] = "Welcome to SitNow"

    response = render(request, "sitnow/index.html", context=context_dict)

    return response


def aboutus(request):
    context_dict = {}
    context_dict["about_msg"] = "About SitNow"

    response = render(request, "sitnow/aboutus.html", context=context_dict)

    return response

def advantages(request):
    context_dict = {}
    context_dict["advantage_msg"] = "Advantages of SitNow"

    response = render(request, "sitnow/advantages.html", context=context_dict)

    return response

def forwhom(request):
    context_dict = {}
    context_dict["forwhom_msg"] = "For Whom SitNow"

    response = render(request, "sitnow/forwhom.html", context=context_dict)

    return response

def tutorial(request):
    context_dict = {}
    context_dict["tutorial_msg"] = "Tutorial SitNow"

    response = render(request, "sitnow/tutorial.html", context=context_dict)

    return response


def forum(request):
    context_dict = {}
    context_dict["forum_msg"] = "forum"

    response = render(request, "sitnow/forum.html", context=context_dict)

    return response

def result(request):
    context_dict = {}
    context_dict["result_msg"] = "result"

    response = render(request, "sitnow/result.html", context=context_dict)

    return response

def favorite(request):
    context_dict = {}
    context_dict["fovorite_msg"] = "favorite"

    response = render(request, "sitnow/favorite.html", context=context_dict)

    return response

def setting(request):
    context_dict = {}
    context_dict["setting_msg"] = "setting"

    response = render(request, "sitnow/setting.html", context=context_dict)

    return response


def register(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == "POST":
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(
        request,
        "sitnow/register.html",
        context={
            "user_form": user_form,
            "profile_form": profile_form,
            "registered": registered,
        },
    )


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == "POST":
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return redirect(reverse("sitnow:index"))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Sit Now account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, "sitnow/login.html")


# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse("sitnow:index"))


def test(request):
    data = {"name": "Vitor", "location": "Finland", "is_active": True, "count": 28}
    return JsonResponse(data)
