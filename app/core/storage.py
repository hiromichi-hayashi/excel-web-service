import logging
import os
import uuid
from pathlib import Path

from app.core.config import settings

logger = logging.getLogger(__name__)


def validate_path(relative_path: str) -> bool:
    """
    パストラバーサル攻撃を防ぐためのパス検証

    Args:
        relative_path: 検証する相対パス

    Returns:
        パスが安全な場合True、危険な場合False
    """
    try:
        # 絶対パスに解決
        upload_dir = Path(settings.UPLOAD_DIR).resolve()
        full_path = (upload_dir / relative_path).resolve()

        # パスがアップロードディレクトリ内にあることを確認
        # Python 3.9+ の is_relative_to() を使用して安全なパス検証
        return full_path.is_relative_to(upload_dir)
    except Exception:
        return False


def get_user_upload_dir(user_id: int) -> Path:
    """ユーザーごとのアップロードディレクトリを取得"""
    upload_dir = Path(settings.UPLOAD_DIR) / str(user_id)
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir


def sanitize_filename(filename: str) -> str:
    """
    ファイル名をサニタイズしてパストラバーサルを防ぐ

    Args:
        filename: 元のファイル名

    Returns:
        サニタイズされたファイル名
    """
    # パス区切り文字を削除
    filename = os.path.basename(filename)

    # 危険な文字を削除または置換
    dangerous_chars = ["..", "/", "\\", "\0"]
    for char in dangerous_chars:
        filename = filename.replace(char, "_")

    # 空白や特殊文字の処理
    filename = filename.strip()

    # 空のファイル名の場合はデフォルト値を返す
    if not filename:
        filename = "unnamed_file"

    return filename


def generate_unique_filename(original_filename: str) -> str:
    """
    一意なファイル名を生成
    形式: uuid_元のファイル名

    Args:
        original_filename: 元のファイル名

    Returns:
        サニタイズされた一意のファイル名
    """
    # ファイル名をサニタイズ
    safe_filename = sanitize_filename(original_filename)

    unique_id = str(uuid.uuid4())[:8]
    return f"{unique_id}_{safe_filename}"


def save_upload_file(user_id: int, file_content: bytes, filename: str) -> str:
    """
    アップロードファイルを保存

    Args:
        user_id: ユーザーID
        file_content: ファイルの内容
        filename: ファイル名

    Returns:
        保存したファイルの相対パス
    """
    user_dir = get_user_upload_dir(user_id)
    unique_filename = generate_unique_filename(filename)
    file_path = user_dir / unique_filename

    with open(file_path, "wb") as f:
        f.write(file_content)

    # 相対パスを返す
    return str(Path(str(user_id)) / unique_filename)


def get_file_path(relative_path: str) -> Path:
    """
    相対パスから絶対パスを取得（パストラバーサル対策付き）

    Args:
        relative_path: ファイルの相対パス

    Returns:
        検証済みの絶対パス

    Raises:
        ValueError: パスが不正な場合
    """
    if not validate_path(relative_path):
        # 詳細なパス情報はサーバーサイドでログに記録
        logger.warning(f"不正なファイルパスが検出されました: {relative_path}")
        # ユーザーには一般的なエラーメッセージのみを返す
        raise ValueError("不正なファイルパスが検出されました")

    return Path(settings.UPLOAD_DIR) / relative_path


def delete_file(relative_path: str) -> bool:
    """
    ファイルを削除

    Args:
        relative_path: ファイルの相対パス

    Returns:
        削除成功したかどうか
    """
    try:
        file_path = get_file_path(relative_path)
        if file_path.exists():
            file_path.unlink()
            return True
        return False
    except Exception:
        return False


def get_file_size(file_path: Path) -> int:
    """ファイルサイズを取得（バイト）"""
    return file_path.stat().st_size if file_path.exists() else 0


def validate_file_extension(filename: str) -> bool:
    """ファイル拡張子が許可されているか検証"""
    ext = os.path.splitext(filename)[1].lower()
    return ext in settings.ALLOWED_EXTENSIONS


def format_file_size(size_bytes: int) -> str:
    """ファイルサイズを人間が読みやすい形式にフォーマット"""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"
