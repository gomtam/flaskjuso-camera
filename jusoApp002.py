from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import os
import base64
import uuid
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# 연락처 데이터 파일 경로
CONTACTS_FILE = 'addrbook.txt'

# 이미지 저장 경로
IMAGE_FOLDER = 'static/images'

# 데이터 구분자
FIELD_SEPARATOR = "|"
RECORD_SEPARATOR = "\n---\n"

# 서버 시작 시 이미지 폴더 생성
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# 연락처 데이터 불러오기
def load_contacts():
    contacts = []
    if os.path.exists(CONTACTS_FILE):
        try:
            with open(CONTACTS_FILE, 'r', encoding='utf-8') as file:
                content = file.read()
                if not content.strip():
                    return []
                
                records = content.split(RECORD_SEPARATOR)
                for record in records:
                    if not record.strip():
                        continue
                    
                    fields = record.strip().split('\n')
                    contact = {}
                    for field in fields:
                        if FIELD_SEPARATOR in field:
                            key, value = field.split(FIELD_SEPARATOR, 1)
                            contact[key.strip()] = value.strip()
                    
                    if 'id' in contact:
                        contact['id'] = int(contact['id'])
                    
                    if contact:  # 빈 딕셔너리가 아니라면 추가
                        contacts.append(contact)
        except Exception as e:
            print(f"파일 읽기 오류: {e}")
            return []
    return contacts

# 연락처 데이터 저장하기
def save_contacts(contacts):
    with open(CONTACTS_FILE, 'w', encoding='utf-8') as file:
        for i, contact in enumerate(contacts):
            # 각 필드를 key|value 형식으로 저장
            for key, value in contact.items():
                file.write(f"{key}{FIELD_SEPARATOR}{value}\n")
            
            # 마지막 레코드가 아니면 구분자 추가
            if i < len(contacts) - 1:
                file.write(RECORD_SEPARATOR)

# 새 연락처 ID 생성 (현재 최대 ID + 1)
def generate_new_id(contacts):
    if not contacts:
        return 1
    return max(contact['id'] for contact in contacts) + 1

@app.route('/')
def index():
    contacts = load_contacts()
    # 이름 기준으로 정렬
    contacts.sort(key=lambda x: x.get('name', ''))
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        birthday = request.form.get('birthday', '')
        photo = request.form.get('photo', '')
        
        if not name:
            flash('이름은 필수입니다!')
            return redirect(url_for('add'))
        
        contacts = load_contacts()
        new_contact = {
            'id': generate_new_id(contacts),
            'name': name,
            'phone': phone,
            'email': email,
            'address': address,
            'birthday': birthday,
            'photo': photo,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        contacts.append(new_contact)
        save_contacts(contacts)
        
        flash('연락처가 추가되었습니다!')
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    contacts = load_contacts()
    contact = next((c for c in contacts if c['id'] == id), None)
    
    if not contact:
        flash('연락처를 찾을 수 없습니다!')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        contact['name'] = request.form['name']
        contact['phone'] = request.form['phone']
        contact['email'] = request.form['email']
        contact['address'] = request.form['address'] 
        contact['birthday'] = request.form.get('birthday', '')
        
        # 사진이 새로 촬영된 경우에만 업데이트
        new_photo = request.form.get('photo', '')
        if new_photo:
            # 기존 사진 파일 삭제
            if 'photo' in contact and contact['photo']:
                try:
                    old_photo_path = contact['photo']
                    if os.path.exists(old_photo_path):
                        os.remove(old_photo_path)
                        print(f"이전 사진 파일 삭제 완료: {old_photo_path}")
                except Exception as e:
                    print(f"기존 사진 삭제 오류: {e}")
                    
            contact['photo'] = new_photo
        
        if not contact['name']:
            flash('이름은 필수입니다!')
            return redirect(url_for('edit', id=id))
        
        save_contacts(contacts)
        flash('연락처가 수정되었습니다!')
        return redirect(url_for('index'))
    
    return render_template('edit.html', contact=contact)

@app.route('/delete/<int:id>')
def delete(id):
    contacts = load_contacts()
    contact = next((c for c in contacts if c['id'] == id), None)
    
    # 연락처에 사진이 있으면 삭제
    if contact and 'photo' in contact and contact['photo']:
        try:
            photo_path = contact['photo']
            if os.path.exists(photo_path):
                os.remove(photo_path)
                print(f"연락처 삭제 시 사진 파일 삭제 완료: {photo_path}")
        except Exception as e:
            print(f"사진 삭제 오류: {e}")
    
    contacts = [c for c in contacts if c['id'] != id]
    save_contacts(contacts)
    
    flash('연락처가 삭제되었습니다!')
    return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    contacts = load_contacts()
    
    if query:
        filtered_contacts = []
        for contact in contacts:
            if (query in contact.get('name', '').lower() or
                query in contact.get('email', '').lower() or
                query in contact.get('phone', '').lower() or
                query in contact.get('address', '').lower() or
                query in contact.get('birthday', '').lower()):
                filtered_contacts.append(contact)
        contacts = filtered_contacts
    
    return render_template('index.html', contacts=contacts, search_query=query)

@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    if 'photo' not in request.json:
        return jsonify({'success': False, 'error': '사진 데이터가 없습니다.'}), 400
    
    try:
        # 이미지 데이터 추출 (Base64 형식)
        image_data = request.json['photo']
        
        # Base64 접두어 제거
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        # 이미지 저장
        if not os.path.exists(IMAGE_FOLDER):
            os.makedirs(IMAGE_FOLDER)
        
        # 고유한 파일명 생성
        filename = f"{uuid.uuid4()}.jpg"
        file_path = os.path.join(IMAGE_FOLDER, filename)
        
        # 이미지 파일 저장
        with open(file_path, 'wb') as f:
            f.write(base64.b64decode(image_data))
        
        # 상대 경로 반환 (슬래시 통일)
        rel_path = file_path.replace('\\', '/')
        
        # 이전에 사용하던 사진이 있으면 삭제 (이 부분은 실제 삭제는 edit 라우트에서 처리)
        return jsonify({'success': True, 'photo_path': rel_path})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)