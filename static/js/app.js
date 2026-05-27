function getCookie(name){return document.cookie.split('; ').find(row=>row.startsWith(name+'='))?.split('=')[1]}
function authHeaders(json=true){const h={'X-CSRFToken':getCookie('csrftoken')||''};if(json)h['Content-Type']='application/json';return h}
async function api(url){
  const response=await fetch(url,{headers:authHeaders(false)})
  if(!response.ok){throw new Error(`Request failed: ${response.status}`)}
  return response.json()
}
function applyTheme(theme){
  document.documentElement.dataset.theme=theme
  localStorage.setItem('theme',theme)
}
applyTheme(localStorage.getItem('theme')||'dark')
document.getElementById('themeToggle')?.addEventListener('click',()=>applyTheme(document.documentElement.dataset.theme==='dark'?'light':'dark'))
