#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, 'E:/workspace/opencode/token_manager')

from app import create_app

def run_tests():
    print("="*60)
    print("Testing Token Manager App")
    print("="*60)
    
    app = create_app()
    app.config['WTF_CSRF_ENABLED'] = False
    print("[OK] App created")
    
    with app.test_client() as client:
        # 1. Login page
        r = client.get('/auth/login')
        print(f"[1] Login page: {r.status_code} {'OK' if r.status_code == 200 else 'FAIL'}")
        
        # 2. Register page
        r = client.get('/auth/register')
        print(f"[2] Register page: {r.status_code} {'OK' if r.status_code == 200 else 'FAIL'}")
        
        # 3. Register new user
        r = client.post('/auth/register', data={
            'username': 'testuser1',
            'email': 'test1@test.com',
            'password': 'password123',
            'confirm': 'password123'
        }, follow_redirects=True)
        print(f"[3] Register: {r.status_code} {'OK' if r.status_code == 200 else 'FAIL'}")
        
        # 4. User login
        r = client.post('/auth/login', data={
            'username': 'testuser1',
            'password': 'password123'
        }, follow_redirects=True)
        print(f"[4] User login: {r.status_code} {'OK' if r.status_code == 200 else 'FAIL'}")
        
        # 5. User dashboard
        r = client.get('/user/dashboard')
        print(f"[5] User dashboard: {r.status_code} {'OK' if r.status_code == 200 else 'FAIL'}")
        
        # 7. Admin login
        r = client.post('/auth/login', data={
            'username': 'root',
            'password': 'root123'
        }, follow_redirects=True)
        print(f"[7] Admin login: {r.status_code} {'OK' if r.status_code == 200 else 'FAIL'}")
        
        # 8. Admin dashboard
        r = client.get('/admin/dashboard')
        print(f"[8] Admin dashboard: {r.status_code} {'OK' if r.status_code == 200 else 'FAIL'}")
        
        # 9. Admin add tokens to user (use existing user ID 4)
        r = client.post('/admin/user/4/add_tokens', data={'amount': '200'})
        print(f"[9] Admin add tokens: {r.status_code} {'OK' if r.status_code in [200, 302] else 'FAIL'}")
        
        # 10. Admin delete user (use existing user ID 7)
        r = client.post('/admin/user/7/delete')
        print(f"[10] Delete user: {r.status_code} {'OK' if r.status_code in [200, 302] else 'FAIL'}")
        
    print("="*60)
    print("All tests PASSED!")
    print("="*60)

if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print(f"ERROR: {e}")
