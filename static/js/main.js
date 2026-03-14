// Token Manager - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // 自动隐藏提示消息
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.remove();
            }, 500);
        }, 5000);
    });

    // 确认删除操作
    const deleteForms = document.querySelectorAll('form[onsubmit*="confirm"]');
    deleteForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!confirm('确定要执行此操作吗？')) {
                e.preventDefault();
            }
        });
    });

    // Token输入验证
    const tokenInputs = document.querySelectorAll('input[name="amount"]');
    tokenInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            const value = parseInt(this.value);
            if (value < 0) {
                this.value = 0;
            }
        });
    });

    // 密码确认验证
    const passwordForms = document.querySelectorAll('form');
    passwordForms.forEach(function(form) {
        if (form.querySelector('input[name="new_password"]') && 
            form.querySelector('input[name="confirm_password"]')) {
            form.addEventListener('submit', function(e) {
                const newPassword = form.querySelector('input[name="new_password"]').value;
                const confirmPassword = form.querySelector('input[name="confirm_password"]').value;
                
                if (newPassword !== confirmPassword) {
                    e.preventDefault();
                    alert('两次输入的密码不一致！');
                }
            });
        }
    });
});
