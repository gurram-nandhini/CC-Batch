from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from database import get_connection
from auth import hash_password, verify_password, create_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(data: RegisterRequest):

    connection = None
    cursor = None

    try:

        connection = get_connection()
        cursor = connection.cursor()

        # Check existing email
        cursor.execute(
            "SELECT id FROM users WHERE email = %s",
            (data.email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        # Hash password
        hashed_password = hash_password(data.password)

        # Insert user
        cursor.execute(
            """
            INSERT INTO users
            (name, email, password)
            VALUES (%s, %s, %s)
            """,
            (
                data.name,
                data.email,
                hashed_password
            )
        )

        connection.commit()

        user_id = cursor.lastrowid

        return {
            "message": "Registration successful",
            "user_id": user_id,
            "name": data.name,
            "email": data.email
        }

    except HTTPException:
        raise

    except Exception as e:

        if connection:
            connection.rollback()

        print("REGISTER ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=f"Registration failed: {str(e)}"
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


@router.post("/login")
def login(data: LoginRequest):

    connection = None
    cursor = None

    try:

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE email = %s
            """,
            (data.email,)
        )

        user = cursor.fetchone()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        if not verify_password(
            data.password,
            user["password"]
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        token = create_token(user["id"])

        return {
            "message": "Login successful",
            "token": token,
            "user_id": user["id"],
            "name": user["name"]
        }

    except HTTPException:
        raise

    except Exception as e:

        print("LOGIN ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=f"Login failed: {str(e)}"
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()