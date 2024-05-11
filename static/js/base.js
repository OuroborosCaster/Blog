window.onload = function () {
    let session_check = Cookies.get('session_check')
    if (!session_check) {
        fetch('/session');
    }
}

expandContent = function () {
    let contentDiv = $('#content');
    let appDiv = $('#app');
    if (contentDiv.outerHeight() < appDiv.outerHeight()) {
        contentDiv.css('height', appDiv.outerHeight() + 'px');
        console.log('已扩展')
    }
    console.log('已触发')
}

resizeContent = function () {
    let navHeight = $('#navbar').outerHeight();
    let footerHeight = $('#footer').outerHeight();
    let contentDiv = $('#content');
    let contentDivOriginalHeight = contentDiv.outerHeight();
    let calHeight = window.innerHeight - navHeight - footerHeight;
    contentDiv.css('height', Math.max(calHeight, contentDivOriginalHeight) + 'px');
    // console.log('宽度改变')
}
var darkmode;

darkmode = new Darkmode();

const base = Vue.createApp({
    data() {
        return {
            isLoggedIn: false
        };
    },
    mounted() {
        // 使主题高度自适应
        window.addEventListener('resize', resizeContent);
        resizeContent();
        // 检查主题模式
        this.customCssBase();
        // 检查登陆状态
        let loginCookie = Cookies.get('user_jwt')
        if (loginCookie) {
            let user_jwt = jwt_decode(loginCookie);

            this.isLoggedIn = true;
            Vue.nextTick(() => {
                let label_nickname = this.$refs.labelNickname;
                if (label_nickname) {
                    label_nickname.innerText = " " + user_jwt['nickname']
                }

            });
            //执行登录cookie更新
            let iat = user_jwt['iat'];
            let exp = user_jwt['exp'];
            let timestamp = Math.floor(new Date().getTime() / 1000);
            if ((exp - iat) < 2592000) {
                // 仅在登录快过期的最后一天执行登陆状态延长
                if ((exp - timestamp) < 86400) {
                    this.renewLoginCookie();
                } else {
                    console.log('无需更新')
                }
            }
        }
    },
    unmounted() {
        window.removeEventListener('resize', resizeContent);
    },
    methods: {
        renewLoginCookie: async function () {
            await fetch('/renew-login')
        },
        logout: function (event) {
            Cookies.remove('user_jwt')
            alert('登出成功')
            location.reload()
        },
        switchTheme: function () {
            darkmode.toggle();
            this.customCssBase();
        },
        customCssBase: function () {
            let icon = document.getElementById("themeIcon");
            let navbar = $('#navbar');
            if (darkmode.isActivated()) {
                icon.classList.remove("fa-sun");
                icon.classList.add("fa-moon");
                navbar.css('background-color', '#000')
            } else {
                icon.classList.remove("fa-moon");
                icon.classList.add("fa-sun");
                navbar.css('background-color', '#eee')
            }
        },
    }
});
// 挂载 Vue 应用到页面上
base.mount('#base');
