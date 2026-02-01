from app.db.session import sessionlocal
from app.db.model import User
from app.Services.auth_services import AuthService

def create_admin():
    db = sessionlocal()
    auth_service = AuthService()
    hashed_password = auth_service.get_password_hash("admin123")  # Change password as needed
    admin_user = User(email="admin@example.com", hashed_password=hashed_password, role="admin", is_active=True)
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    print("Admin user created:", admin_user.email)
    db.close()

if __name__ == "__main__":
    create_admin()
