customCssEditor = function () {
    $(function () {
        let vditor = document.getElementById('editor').contentWindow.vditor;
        if (darkmode.isActivated()) {
            vditor.setTheme('dark', 'dark')
        } else {
            vditor.setTheme('light', 'light')
        }
    })
}
let loginCookie = Cookies.get('user_jwt')
if (!loginCookie) {
    alert("请登录后使用该功能!");
    location.href = "/login"
}
let user_jwt = jwt_decode(loginCookie);
let uid = user_jwt['uid']
$(function () {
    const app = Vue.createApp({
        data() {
            return {
                isSubmitting: false,
                title: localStorage.getItem(uid + '_title') || '',
                summary: localStorage.getItem(uid + '_summary') || ''
            }
        },
        mounted() {

            $('#themeButton').click(() => {
                customCssEditor();
            });
        },
        methods: {
            cacheTitle: async function () {
                localStorage.setItem(uid + '_title', this.title);
            },
            cacheSummary: async function () {
                localStorage.setItem(uid + '_summary', this.summary);
            },
            checkInput: function (str) {
                const format = /[^\p{L}\p{N}\p{P} \n\t]/gu;
                return format.test(str);
            },
            save: async function (event) {
                event.preventDefault()
                await this.cacheTitle();
                await this.cacheSummary()
                let vditor = document.getElementById('editor').contentWindow.vditor;
                localStorage.setItem(uid + '_content', vditor.getValue())
                UIkit.notification({
                    message: `已保存`,
                    status: 'success',
                    timeout: 500,
                    pos: 'top-center'
                });
            },
            clear: async function (event) {
                if (event) {
                    event.preventDefault();
                }
                localStorage.removeItem(uid + '_title');
                this.title = '';
                localStorage.removeItem(uid + '_summary');
                this.summary = '';
                let vditor = document.getElementById('editor').contentWindow.vditor;
                localStorage.removeItem(uid + '_content');
                vditor.setValue('')
            },
            publish: async function (event) {
                event.preventDefault()
                this.isSubmitting = true;
                let vditor = document.getElementById('editor').contentWindow.vditor;
                const content = vditor.getValue()
                try {
                    if (this.title.trim() === '') {
                        throw new Error(`标题不可为空`);
                    } else if (content.trim() === '') {
                        throw new Error(`正文不可为空`);
                    } else if (this.checkInput(this.title.trim())) {
                        throw new Error(`标题不可使用特殊字符`);
                    } else if (this.checkInput(this.summary.trim())) {
                        throw new Error(`简介不可使用特殊字符`);
                    } else {
                        let article_data = {
                            'title': this.title.trim(),
                            'summary': this.summary.trim(),
                            'content': content.trim()
                        }
                        const response = await fetch('/api/article/publish', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(article_data)
                        });
                        if (response.status !== 200) {
                            let data = await response.json();
                            throw new Error(` ${response.status}-${data.detail}`);
                        }
                        UIkit.notification({
                            message: '<div style="text-align: center">发布成功，正在跳转<br>' +
                                '<i class="fas fa-spinner fa-spin"></i></div>',
                            status: 'success',
                            timeout: 2000,
                            pos: 'top-center'
                        });
                        await this.clear();
                        setTimeout(() => {
                            this.isSubmitting = false;
                            location.href = '/'
                        }, 1500);
                    }
                } catch (e) {
                    UIkit.notification({
                        message: `${e}`,
                        status: 'danger',
                        timeout: 5000,
                        pos: 'top-center'
                    });
                    this.isSubmitting = false;
                    return;
                }

            }
        }
    })
    app.mount('#app');
})