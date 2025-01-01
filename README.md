# MrHiddenFastApi
    ایجاد یک ای پی ای برای ذخیره اطلاعات مقالات و .... سایت آینده من

# ایجاد مایگریتشن 
    alembic revision --autogenerate -m ""


app/
.... config/
........ db_config.py (engine, async_session, create_db_and_tables, get_session, SessionDep)
.... models/
........ blog_model.py(Blog)
........ user_model.py (USER)
.... routers/
........ authenticate.py (get_password_hash, verify_password, verify_user_credentials, create_access_token, login)
........ blog_router.py (create_blog, read_blogs, read_blog, update_blog, delete_blog)
........ user_router.py (update_user_helper, create_user, create_staffuser, create_superuser, read_users, read_user, update_user, update_staffuser, update_superuser, update_owner, delete_user)
.... schemas/
........ authenticate_schema.py (AuthenticateCreate, AuthenticateRead)
........ blog_schema.py (BlogCreate, BlogRead, BlogUpdate, )
........ user_schema.py (BaseUserCreate, StaffUserCreate, SuperuserCreate, BaseUser, UserRead, StaffUserRead, SuperuserRead, OwnerRead, BaseUserUpdate, StaffUserUpdate, SuperuserUpdate, OwnerUpdate)
.... main.py (app)
.... database.db
.... requirements.txt


http://62.3.41.209:3000/docs
http://62.3.41.209:3000/redoc

اول برای هر کاری باید authenticate کنی از این آدرس
http://62.3.41.209:3000/authenticate/gettoken/


fetch('http://62.3.41.209:3000/authenticate/gettoken/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        'username': 'admin',
        'password': 'admin'
    })
})
.then(response => response.json())
.then(data => {
    console.log(data);
    localStorage.setItem('access_token', data.access_token);
})
.catch(error => console.error('Error:', error));

خب تا اینجا اومدم توی لوکال استوریج توکن رو سیو کردیم حالا می تونیم از توی همون قسمت بریم و ازش استفاده کنیم


const token = localStorage.getItem('access_token');

fetch('http://62.3.41.209:3000/normalusers/', {
    method: 'GET',
    headers: {
        'Authorization': `Bearer ${token}`
    }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));


یه راه ذخیره سازی دیگه هم اینه که بیاییم توی سشن ها این توکن دریافتی رو ذخیره کنیم این طوری

fetch('http://62.3.41.209:3000/authenticate/gettoken/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        'username': 'admin',
        'password': 'admin'
    })
})
.then(response => response.json())
.then(data => {
    console.log(data);
    sessionStorage.setItem('access_token', data.access_token);
})
.catch(error => console.error('Error:', error));


پس برای استفاده ازش هم باید از این دستور استفاده کنیم

const token = sessionStorage.getItem('access_token');

fetch('http://62.3.41.209:3000/normalusers/', {
    method: 'GET',
    headers: {
        'Authorization': `Bearer ${token}`
    }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));