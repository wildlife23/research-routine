import smtplib
import os
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email_smtp(to, subject, body, attachment_path=None):
    gmail_address = os.environ.get("GMAIL_ADDRESS")
    gmail_app_password = os.environ.get("GMAIL_APP_PASSWORD")

    if not gmail_address or not gmail_app_password:
        print("❌ 환경변수 GMAIL_ADDRESS 또는 GMAIL_APP_PASSWORD가 설정되지 않았습니다.")
        sys.exit(1)

    msg = MIMEMultipart()
    msg['From'] = gmail_address
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            filename = os.path.basename(attachment_path)
            part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
            msg.attach(part)
        print(f"📎 첨부파일 추가: {attachment_path}")
    else:
        if attachment_path:
            print(f"⚠️ 첨부파일을 찾을 수 없습니다: {attachment_path}")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(gmail_address, gmail_app_password)
            smtp.send_message(msg)
        print(f"✅ 이메일 발송 완료 → {to}")
    except smtplib.SMTPAuthenticationError:
        print("❌ 인증 실패: 앱 비밀번호를 확인하세요.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 발송 실패: {e}")
        sys.exit(1)

if __name__ == '__main__':
    # 사용법: python send_email.py <받는사람> <제목> <첨부파일경로>
    if len(sys.argv) < 4:
        print("사용법: python send_email.py <to> <subject> <attachment_path>")
        sys.exit(1)

    to = sys.argv[1]
    subject = sys.argv[2]
    attachment_path = sys.argv[3]

    body = f"""안녕하세요,

이번 주 논문 리뷰 보고서를 첨부드립니다.

보고서 파일명: {os.path.basename(attachment_path)}
발송일: {attachment_path.split('-weekly')[0].split('/')[-1] if 'weekly' in attachment_path else ''}

확인 부탁드립니다.

※ 이 메일은 자동 발송되었습니다.
"""
    send_email_smtp(to, subject, body, attachment_path)
