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