$(function () {
    const app = Vue.createApp({

            data: function () {
                return {
                    isSubmitting: false,
                    loginMethod: 'username',
                    identity: '',
                    email: '',
                    password: '',
                };
            },
            mounted() {
                let loginCookie = Cookies.get('user_jwt')
                if (loginCookie) {
                    alert("您已登录，若要切换账号请先登出");
                    location.href = '/'
                }
                this.customCssLog();
                $('#themeButton').click(() => {
                    this.customCssLog();

                });
            },
            methods: {
                preventSpace: function (event) {
                    if (event.key === ' ') {
                        event.preventDefault();
                    }
                },
                switchLogin: function () {
                    try {
                        const identityField = document.getElementById('identity-field');
                        const identityIconField = document.getElementById('identity-icon');
                        if (this.loginMethod === 'email') {
                            identityField.placeholder = '电子邮箱';
                            identityField.maxLength = 50;
                            identityIconField.innerHTML = '<i class="fa-regular fa-envelope"></i>';
                        } else if (this.loginMethod === 'username') {
                            identityField.placeholder = '用户名';
                            identityField.maxLength = 16;
                            identityIconField.innerHTML = '<i class="fa-solid fa-user"></i>';
                        } else {
                            throw new Error(`无效的值`);
                        }
                    } catch (e) {
                        UIkit.notification({
                            message: `出现错误：${e}`,
                            status: 'danger',
                            timeout: 5000,
                            pos: 'top-center'
                        })

                    }
                },
                login: async function (event) {
                    event.preventDefault()
                    this.isSubmitting = true;
                    let user_data;
                    try {
                        if (this.loginMethod === 'email') {
                            if (this.identity === '') {
                                throw new Error(`请提供邮箱`);
                            }
                            const format = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
                            if (!format.test(this.identity)) {
                                throw new Error(`邮箱格式不正确`);
                            }
                            if (this.password === '') {
                                throw new Error(`请输入密码`);
                            }
                            user_data = {
                                "email": this.identity.trim(),
                                "password": this.password.trim(),
                            }
                        } else if (this.loginMethod === 'username') {
                            if (this.identity === '') {

                                throw new Error(`请提供用户名`);
                            }
                            if (this.identity === '') {
                                throw new Error(`请输入密码`);
                            }
                            user_data = {
                                "username": this.identity.trim(),
                                "password": this.password.trim(),
                            }
                        } else {
                            throw new Error(`不规范的操作`);
                        }
                    } catch (e) {
                        UIkit.notification({
                            message: `${e}`,
                            status: 'danger',
                            timeout: 500,
                            pos: 'top-center'
                        });
                        return;
                    }
                    try {
                        const response = await fetch('/api/login', {
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
                            message: '<div style="text-align: center">登录成功，正在跳转<br>' +
                                '<i class="fas fa-spinner fa-spin"></i></div>',
                            status: 'success',
                            timeout: 2000,
                            pos: 'top-center'
                        });
                        setTimeout(() => {
                            this.isSubmitting = false;
                            location.href = '/'
                        }, 1500);
                    } catch (e) {
                        UIkit.notification({
                            message: `登录失败，错误信息： ${e}`,
                            status: 'danger',
                            timeout: 5000,
                            pos: 'top-center'
                        });
                        this.isSubmitting = false;
                    }
                },
                customCssLog: function () {
                    let log = $('#app');
                    let button = $('#submitButton');
                    if (darkmode.isActivated()) {
                        log.removeClass('uk-card-default')
                        log.addClass('uk-card-secondary')
                        button.removeClass('uk-button-primary')
                        button.addClass('uk-button-default')
                    } else {
                        log.removeClass('uk-card-secondary')
                        log.addClass('uk-card-default')
                        button.removeClass('uk-button-default')
                        button.addClass('uk-button-primary')
                    }
                }
            }
        }
    )
    app.mount('#app');
});
