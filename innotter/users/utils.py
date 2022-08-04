from datetime import datetime, timedelta

from rest_framework import status

import jwt

from innotter.settings import JWT_SECRET, JWT_ACCESS_TTL, JWT_REFRESH_TTL
from innotter.aws import s3
from innotter.settings import AWS
 
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
    

def update_user_avatar(request, pk):
    IMAGE_EXTS = ("png", "jpg", "jpeg", "gif")
    user = request.user
    if int(user.pk) != int(pk):
        return {"Error": "Wrong user id."}, status.HTTP_400_BAD_REQUEST    

    file = request.FILES["img"]
    file_ext = file.name.split(".")[-1]
    if not file_ext in IMAGE_EXTS:
        return {"Error": f"Invalid file extension .{file_ext} ."}, status.HTTP_400_BAD_REQUEST 

    timestamp = int(datetime.now().timestamp())
    s3_key = file.name + "_" +str(user.pk)+str(timestamp)+"."+file_ext

    s3.put_object(
        Bucket=AWS["AWS_BUCKET_NAME"],
        Key=s3_key,
        Body=file
    )

    s3_image_path = f"s3://{AWS['AWS_BUCKET_NAME']}/{s3_key}"

    user.image_s3_path = s3_key
    user.save()
    
    exp_time = 60 * 60 * 24 * 7
    url = s3.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": AWS["AWS_BUCKET_NAME"],
            "Key": s3_key
        },
        ExpiresIn=exp_time
    )

    return {"avatar_url": url}, status.HTTP_200_OK
 
        