document.addEventListener('DOMContentLoaded', async function () {
    const themeToggle = document.getElementById('theme-toggle')
    const themeIcon = document.getElementById('theme-icon')
    let theme = localStorage.getItem('theme') || 'light' // Load from localStorage

    applyTheme(theme)

    // Fetch user theme if logged in
    try {
        const response = await fetch('http://127.0.0.1:8008/get-user-theme/')
        if (response.ok) {
            const data = await response.json()
            if (data.theme && data.theme !== theme) {
                theme = data.theme
                localStorage.setItem('theme', theme)
                applyTheme(theme)
            }
        }
    } catch (error) {
        console.warn('Not logged in or error fetching theme. Using LocalStorage theme.')
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', async () => {
            theme = theme === 'dark' ? 'light' : 'dark'
            localStorage.setItem('theme', theme)
            applyTheme(theme)

            // Update theme in database if logged in
            try {
                const csrfToken = getCookie('csrftoken')
                if (csrfToken) {
                    await fetch('http://127.0.0.1:8008/set-user-theme/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken
                        },
                        body: JSON.stringify({ theme })
                    })
                } else {
                    console.warn('CSRF token not found. Theme update request may fail.')
                }
            } catch (error) {
                console.warn('Error updating theme in database.')
            }
        })
    }

    function applyTheme(theme) {
        document.documentElement.classList.remove('dark', 'light')
        document.documentElement.classList.add(theme)

        if (themeIcon) {
            themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙'
        }
    }

    function getCookie(name) {
        let cookieValue = null
        if (document.cookie) {
            const cookies = document.cookie.split(';')
            for (let cookie of cookies) {
                cookie = cookie.trim()
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                    break
                }
            }
        }
        return cookieValue
    }
})
