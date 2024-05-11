$(function () {
    const app = Vue.createApp({

        data: function () {
            return {
                isSubmitting: false,
                username: '',
                nickname: '',
                email: '',
                password: '',
                rePassword: ''
            };
        },
        mounted() {
            let loginCookie = Cookies.get('user_jwt');
            if (loginCookie) {
                alert("您已登录，若要注册新账号请先登出");
                location.href = '/'
            }

        },

        methods: {
            preventSpace: function (event) {
                if (event.key === ' ') {
                    event.preventDefault();
                }
            },
            checkUsername: async function () {
                try {
                    const alertUsername = document.getElementById('alert-username');

                    const format = /\s/g
                    if (format.test(this.username)) {
                        alertUsername.className = 'uk-width-1-3@s uk-width-1-1@xs uk-alert uk-alert-no-border uk-margin-left uk-alert-danger';
                        alertUsername.innerHTML = '<i class="fa-solid fa-circle-xmark"></i>&nbsp请不要使用空格';
                        return false;
                    }
                    if (this.username === '') {
                        alertUsername.className = 'uk-width-1-3@s uk-width-1-1@xs uk-alert uk-alert-no-border uk-margin-left uk-alert-danger';
                        alertUsername.innerHTML = '<i class="fa-solid fa-circle-xmark"></i>&nbsp这是必填项'
                        return false;
                    }
                    const response = await fetch('/api/check/username', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({username: this.username})
                    });
                    if (response.status !== 200) {
                        let data = await response.json();
                        throw new Error(` ${response.status}-${data.detail}`);
                    }
                    const result = await response.json();

                    if (result.isAvailable) {
                        alertUsername.className = 'uk-width-1-3@s uk-width-1-1@xs uk-alert uk-alert-no-border uk-margin-left uk-alert-success';
                        alertUsername.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
                    } else {
                        alertUsername.className = 'uk-width-1-3@s uk-width-1-1@xs uk-alert uk-alert-no-border uk-margin-left uk-alert-danger';
                        alertUsername.innerHTML = '<i class="fa-solid fa-circle-xmark"></i>&nbsp用户名已被占用';
                    }
                    return result.isAvailable;
                } catch (e) {
                    UIkit.notification({
                        message: `出现错误： ${e}`,
                        status: 'danger',
                        timeout: 5000,
                        pos: 'top-center'
                    })
                    console.log(`checkUsername ${e}`)
                    return false
                }
            },
            checkNickname: async function () {
                try {
                    const alertNickname = document.getElementById('alert-nickname');
                    const format = /\s/g
                    if (format.test(this.nickname)) {
                        alertNickname.className = 'uk-width-1-3@s uk-width-1-1@xs uk-alert uk-alert-no-border uk-margin-left uk-alert-danger';
                        alertNickname.innerHTML = '<i class="fa-solid fa-circle-xmark"></i>&nbsp请不要使用空格';
                        return false;
                    }

                    if (this.nickname === '') {
                        alertNickname.className = 'uk-width-1-3@s uk-width-1-1@xs uk-alert uk-alert-no-border uk-margin-left ';
                        alertNickname.innerHTML = '&nbsp'
                        return true;
                    }
                    const response = await fetch('/api/check/nickname', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({nickname: this.nickname})
                    });
                    if (response.status !== 200) {
                        let data = await response.json();
                        throw new Error(` ${response.status}-${data.detail}`);
                    }
                    const result = await response.json();

                    if (result.isAvailable) {
                        alertNickname.className = 'uk-width-1-3@s uk-width-1-1@xs uk-alert uk-alert-no-border uk-margin-left uk-alert-success';
                        alertNickname.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
                    } else {
                        alertNickname.className = 'uk-width-1-3@s uk-width-1-1@xs uk-alert uk-alert-no-border uk-margin-left uk-alert-danger';
                        alertNickname.innerHTML = '<i class="fa-solid fa-circle-xmark"></i>&nbsp昵称已被占用';
                    }
                    return result.isAvailable;
                } catch (e) {
                    UIkit.notification({
                        message: `出现错误： ${e}`,
                        status: 'danger',
                        timeout: 5000,
                        pos: 'top-center'
                    })
                    console.log(`checkNickname ${e}`)
                    return false
                }

            },
            checkEmail: async function () {
                try {
                    const alertEmail = document.getElementById('alert-email');
                    if (this.email === '') {
                        alertEmail.className = 'uk-width-1-3@s uk-width-1-1@xs uk-alert uk-alert-no-border uk-margin-left uk-alert-danger';
                        alertEmail.innerHTML = '<i class="fa-solid fa-circle-xmark"></i>&nbsp这是必填项'
                        return false;
                    }
                    const format = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
                    if (!format.test(this.email)) {
                        alertEmail.className = 'uk-width-1-3@s uk-width-1-1@xs uk-alert uk-alert-no-border uk-margin-left uk-alert-danger';
                        alertEmail.innerHTML = '<i class="fa-solid fa-circle-xmark"></i>&nbsp邮箱格式不正确';
                        return false;
                    }
                    const response = await fetch('/api/check/email', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({email: this.email})
                    });
                    if (response.status !== 200) {
                        let data = await response.json();
                        throw new Error(` ${response.status}-${data.detail}`);
                    }
                    const result = await response.json();

                    if (result.isAvailable) {
                        alertEmail.className = 'uk-width-1-3@s uk-width-1-1@xs uk-alert uk-alert-no-border uk-margin-left uk-alert-success';
                        alertEmail.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
                    } else {
                        alertEmail.className = 'uk-width-1-3@s uk-width-1-1@xs uk-alert uk-alert-no-border uk-margin-left uk-alert-danger';
                        alertEmail.innerHTML = '<i class="fa-solid fa-circle-xmark"></i>&nbsp该邮箱已被注册';
                    }
                    return result.isAvailable;
                } catch (e) {
                    UIkit.notification({
                        message: `出现错误： ${e}`,
                        status: 'danger',
                        timeout: 5000,
                        pos: 'top-center'
                    })
                    console.log(`checkEmail ${e}`)
                    return false
                }
            },
            checkPassword: function () {
                try {
                    const alertPassword = document.getElementById('alert-password');
                    if (this.password === '') {
                        alertPassword.className = 'uk-width-1-3@s uk-width-1-1@xs uk-alert uk-alert-no-border uk-margin-left uk-alert-danger';
                        alertPassword.innerHTML = '<i class="fa-solid fa-circle-xmark"></i>&nbsp这是必填项'
                        return false;
                    }
                    const format = /[^\x21-\x7E]/g
                    if (format.test(this.password)) {
                        alertPassword.className = 'uk-width-1-3@s uk-width-1-1@xs uk-alert uk-alert-no-border uk-margin-left uk-alert-danger';
                        alertPassword.innerHTML = '<i class="fa-solid fa-circle-xmark"></i>&nbsp请仅使用英文字母、英文标点与数字';
                        return false;
                    }
                    if (this.password.length < 8) {
                        alertPassword.className = 'uk-width-1-3@s uk-width-1-1@xs uk-alert uk-alert-no-border uk-margin-left uk-alert-warning';
                        alertPassword.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i>&nbsp密码至少要8位'
                        return false;
                    }
                    if (this.password === this.email || this.password === this.nickname || this.password === this.username) {
                        alertPassword.className = 'uk-width-1-3@s uk-width-1-1@xs uk-alert uk-alert-no-border uk-margin-left uk-alert-warning';
                        alertPassword.innerHTML = '<i class="fas fa-warning"></i>&nbsp不可用用户名、昵称或电子邮箱作为密码'
                        return false;
                    }
                    let types = 0;
                    if (/[\u0021-\u002F\u003A-\u0040\u005B-\u0060\u007B-\u007E]/.test(this.password)) {
                        types++; // 英文标点
                    }
                    if (/[\u0030-\u0039]/.test(this.password)) {
                        types++; // 数字
                    }
                    if (/[\u0041-\u005A\u0061-\u007A]/.test(this.password)) {
                        types++; // 英文字母
                    }
                    if (types < 2) {
                        alertPassword.className = 'uk-width-1-3@s uk-width-1-1@xs uk-alert uk-alert-no-border uk-margin-left uk-alert-warning';
                        alertPassword.innerHTML = '<i class="fas fa-warning"></i>&nbsp密码强度弱,请使用英文字母、英文标点与数字中的至少两种'
                        return false;
                    }
                    alertPassword.className = 'uk-width-1-3@s uk-width-1-1@xs uk-alert uk-alert-no-border uk-margin-left uk-alert-success';
                    alertPassword.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
                    return true;
                } catch (e) {
                    UIkit.notification({
                        message: `出现错误： ${e}`,
                        status: 'danger',
                        timeout: 5000,
                        pos: 'top-center'
                    })
                    console.log(`checkPassword ${e}`)
                    return false
                }
            },
            checkRePassword: function () {
                try {
                    const alertRePassword = document.getElementById('alert-rePassword');
                    if (this.rePassword === '') {
                        alertRePassword.className = 'uk-width-1-3@s uk-width-1-1@xs uk-alert uk-alert-no-border uk-margin-left uk-alert-danger';
                        alertRePassword.innerHTML = '<i class="fa-solid fa-circle-xmark"></i>&nbsp这是必填项'
                        return false;
                    }
                    if (this.rePassword === this.email || this.rePassword === this.nickname || this.rePassword === this.username) {
                        alertRePassword.className = 'uk-width-1-3@s uk-width-1-1@xs uk-alert uk-alert-no-border uk-margin-left uk-alert-warning';
                        alertRePassword.innerHTML = '<i class="fas fa-warning"></i>&nbsp不可用用户名、昵称或电子邮箱作为密码'
                        return false;
                    }
                    if (this.rePassword === this.password) {
                        alertRePassword.className = 'uk-width-1-3@s uk-width-1-1@xs uk-alert uk-alert-no-border uk-margin-left uk-alert-success';
                        alertRePassword.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
                        return true;
                    } else {
                        alertRePassword.className = 'uk-width-1-3@s uk-width-1-1@xs uk-alert uk-alert-no-border uk-margin-left uk-alert-danger';
                        alertRePassword.innerHTML = '<i class="fa-solid fa-circle-xmark"></i>&nbsp两次输入的密码不一致';
                        return false;
                    }
                } catch (e) {
                    UIkit.notification({
                        message: `出现错误： ${e}`,
                        status: 'danger',
                        timeout: 5000,
                        pos: 'top-center'
                    })
                    console.log(`checkRePassword ${e}`)
                    return false
                }
            },
            register: async function (event) {
                event.preventDefault()
                this.isSubmitting = true;
                const isUsernameAvailable = await this.checkUsername();
                const isNicknameAvailable = await this.checkNickname();
                const isEmailAvailable = await this.checkEmail();
                const isPasswordValid = this.checkPassword();
                const isRePasswordValid = this.checkRePassword();
                if (isUsernameAvailable && isNicknameAvailable && isEmailAvailable && isPasswordValid && isRePasswordValid) {
                    const user_data = {
                        "username": this.username.trim(),
                        "nickname": this.nickname.trim() || null,
                        "email": this.email.trim(),
                        "password": this.password.trim(),
                    }
                    try {
                        const response = await fetch('/api/register', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(user_data)
                        });
                        if (response.status !== 200) {
                            let data = await response.json();
                            throw new Error(` ${response.status}-${data.detail}`);
                        }
                        UIkit.notification({
                            message: '<div style="text-align: center">注册成功，3秒后跳转到登录页面<br>' +
                                '<i class="fas fa-spinner fa-spin"></i></div><br>' +
                                '<a href="/login">点击直接跳转</a>',
                            status: 'success',
                            timeout: 5000,
                            pos: 'top-center'
                        });
                        setTimeout(() => {
                            this.isSubmitting = false;
                            location.href = '/login'
                        }, 2500); // 设置3秒的延迟
                        return response.data;
                    } catch (e) {
                        UIkit.notification({
                            message: `注册失败，错误信息： ${e}`,
                            status: 'danger',
                            timeout: 5000,
                            pos: 'top-center'
                        });
                        this.isSubmitting = false;
                    }

                }
            },
            // customCssReg: function () {
            //     let button = $('button');
            //     if (darkmode.isActivated()) {
            //         button.removeClass('uk-button-primary')
            //         button.addClass('uk-button-default')
            //     } else {
            //         button.removeClass('uk-button-default')
            //         button.addClass('uk-button-primary')
            //     }
            // }
        }
    })
    app.mount('#app');

})