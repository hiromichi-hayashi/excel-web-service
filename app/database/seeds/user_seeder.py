"""
ユーザーテーブルのシーダー

使用方法:
    docker compose exec app python -m app.database.seeds.user_seeder
"""

import sys
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlmodel import Session, select

from app.core.security import get_password_hash
from app.database import engine
from app.models.user import User


def seed_users():
    """ユーザーデータを投入"""
    with Session(engine) as db:
        try:
            # 既存のユーザーを確認
            statement = select(User)
            existing_users = len(db.exec(statement).all())
            if existing_users > 0:
                print(f"既に {existing_users} 件のユーザーが存在します。")
                response = input("既存データを削除して再投入しますか？ (y/N): ")
                if response.lower() == "y":
                    # すべてのユーザーを削除
                    for user in db.exec(statement).all():
                        db.delete(user)
                    db.commit()
                    print("既存ユーザーを削除しました。")
                else:
                    print("シーダー実行をキャンセルしました。")
                    return

            # テストユーザーを作成
            users = [
                {
                    "email": "admin@example.com",
                    "username": "admin",
                    "password": "admin123",
                },
                {
                    "email": "user1@example.com",
                    "username": "user1",
                    "password": "user123",
                },
                {
                    "email": "user2@example.com",
                    "username": "user2",
                    "password": "user123",
                },
            ]

            for user_data in users:
                password = user_data.pop("password")
                user = User(**user_data, password=get_password_hash(password))
                db.add(user)

            db.commit()
            print(f"✅ {len(users)} 件のユーザーを登録しました。")
            print("\n登録ユーザー:")
            for user_data in users:
                print(f"  - {user_data['username']} ({user_data['email']})")

        except Exception as e:
            db.rollback()
            print(f"❌ エラーが発生しました: {e}")
            raise


if __name__ == "__main__":
    print("ユーザーシーダーを実行します...")
    seed_users()
    print("完了しました。")
