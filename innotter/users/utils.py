from datetime import datetime, timedelta

from rest_framework import status

import jwt

from innotter.settings import JWT_SECRET, JWT_ACCESS_TTL, JWT_REFRESH_TTL, AWS, IMAGE_EXTS
from innotter.aws import s3
 
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
    

def get_presigned_url(key: str) -> str:
    
    exp_time = 60 * 60 * 24 * 7
    
    url = s3.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": AWS.get("AWS_BUCKET_NAME"),
            "Key": key
        },
        ExpiresIn=exp_time
    )
    
    return url


def put_file_in_bucket(key: str, file) -> None:
    s3.put_object(
        Bucket=AWS.get("AWS_BUCKET_NAME"),
        Key=key,
        Body=file
    )

def create_s3_key(file: str, user: User, file_ext: str) -> str:
    timestamp = int(datetime.now().timestamp())
    s3_key = file.name + "_" +str(user.pk)+str(timestamp)+"."+file_ext
    
    return s3_key 
    

def update_user_avatar(request, pk):
    user = request.user
    
    if int(user.pk) != int(pk):
        return {"Error": "Wrong user id."}, status.HTTP_400_BAD_REQUEST    

    file = request.FILES["img"]
    file_ext = file.name.split(".")[-1]
    
    if not file_ext in IMAGE_EXTS:
        return {"Error": f"Invalid file extension .{file_ext} ."}, status.HTTP_400_BAD_REQUEST 

    s3_key = create_s3_key(file=file, user=user, file_ext=file_ext)
    put_file_in_bucket(key=s3_key, file=file)
    
    user.image_s3_path = s3_key
    user.save()
    
    presigned_url = get_presigned_url(key=s3_key)
    
    return {"avatar_url": presigned_url}, status.HTTP_200_OK
 
        