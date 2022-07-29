from datetime import datetime, timedelta

import jwt

from innotter.settings import JWT_SECRET, JWT_ACCESS_TTL, JWT_REFRESH_TTL
from mainapp.models import Page
from users.models import User 


def create_jwt_token_dict(to_refresh: bool, validated_data) -> dict:
    
    jwt_token_dict = {
        "access": generate_jwt_token(is_access=True, to_refresh=to_refresh, validated_data=validated_data),
        "refresh": generate_jwt_token(is_access=False, to_refresh=to_refresh, validated_data=validated_data)
    }
    
    return jwt_token_dict


def generate_jwt_token(is_access: bool, to_refresh: bool, validated_data) -> str:
    payload = create_payload(is_access=is_access, to_refresh=to_refresh, validated_data=validated_data)
    token = jwt.encode(payload=payload, key=JWT_SECRET)
    
    return token
    

def create_payload(is_access: bool, to_refresh: bool, validated_data) -> dict:
    payload = {
        "iss": "backend-api",
        "user_id": validated_data["payload"]["user_id"] if to_refresh else validated_data["user"].id,
        "exp": datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TTL if is_access else JWT_REFRESH_TTL),
        "token_type": "access" if is_access else "refresh"
    }
    
    return payload


def block_or_unblock_owner_pages(user: User):
    pages = Page.objects.filter(owner=user)
    
    for page in pages:
        page.is_blocked = user.is_blocked
        page.save()

        
def access_to_admin_panel(user: User) -> bool:
    if user.role == User.Roles.ADMIN:
        user.is_staff = True
        user.is_superuser = True 
        user.save()
        return True
    else:
        user.is_staff = False
        user.is_superuser = False
        user.save()
        return False 
        