from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import auth
from django.contrib.auth import views as auth_views  # 追加
from .forms import (
    LoginForm, 
    SignUpForm, 
    TalkForm,
    UsernameChangeForm,
    EmailChangeForm,
)
from django.contrib.auth.decorators import login_required
from .models import Talk, User
from django.db.models import Q  
from django.urls import reverse_lazy  

class LoginView(auth_views.LoginView):
    authentication_form = LoginForm  # ログイン用のフォームを指定
    template_name = "main/login.html"

def index(request):
    return render(request, "main/index.html")


def signup(request):
    if request.method == "GET":
        form = SignUpForm()
    elif request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save() 
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
            return redirect("index")

    context = {"form": form}
    return render(request, "main/signup.html", context)

def login(request):
    return render(request, "main/login.html")

@login_required
def friends(request):
    friends = User.objects.all()
    context = {
        "friends" : friends,
    }
    return render(request, "main/friends.html", context)

@login_required
def talk_room(request, user_id):
    # get_object_or_404 は、第一引数にモデル名、その後任意の数のキーワードを受け取り、
    # もし合致するデータが存在するならそのデータを、存在しないなら 404 エラーを発生させます。
    friend = get_object_or_404(User, id=user_id)

    # 自分が送信者で上の friend が受信者であるデータ、または friend が送信者で friend が受信者であるデータをすべて取得します。
    talks = Talk.objects.filter(
        Q(sender=request.user, receiver=friend)
        | Q(sender=friend, receiver=request.user)
    ).order_by("time")

    if request.method == "GET":
        form = TalkForm()
    elif request.method == "POST":
        # 送信内容を取得
        form = TalkForm(request.POST)
        if form.is_valid():
            # トークを仮作成
            new_talk = form.save(commit=False)
            # 送信者、受信者、メッセージを与えて保存
            new_talk.sender = request.user
            new_talk.receiver = friend
            new_talk.save()
            return redirect("talk_room", user_id)

    context = {
        "form": form,
        "friend": friend,
        "talks": talks,
    }
    return render(request, "main/talk_room.html", context)

@login_required
def settings(request):
    return render(request, "main/settings.html")

@login_required
def username_change(request):
    if request.method == "GET":
        # instance を指定することで、指定したインスタンスのデータにアクセスできます
        form = UsernameChangeForm(instance=request.user)
    elif request.method == "POST":
        form = UsernameChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # 保存後、完了ページに遷移します
            return redirect("username_change_done")

    context = {"form": form}
    return render(request, "main/username_change.html", context)


@login_required
def username_change_done(request):
    return render(request, "main/username_change_done.html")

@login_required
def email_change(request):
    if request.method == "GET":
        form = EmailChangeForm(instance=request.user)
    elif request.method == "POST":
        form = EmailChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("email_change_done")

    context = {"form": form}
    return render(request, "main/email_change.html", context)

@login_required
def email_change_done(request):
    return render(request, "main/email_change_done.html")

class PasswordChangeView(auth_views.PasswordChangeView):
    """Django 組み込みパスワード変更ビュー

    template_name : 表示するテンプレート
    success_url : 処理が成功した時のリダイレクト先
    """

    template_name = "main/password_change.html"
    success_url = reverse_lazy("password_change_done")


class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    """Django 標準パスワード変更ビュー"""

    template_name = "main/password_change_done.html"

class LogoutView(auth_views.LogoutView):
    pass