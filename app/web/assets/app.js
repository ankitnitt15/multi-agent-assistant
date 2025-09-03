const el = sel => document.querySelector(sel);
const messages = el('#messages');
const form = el('#chat-form');
const input = el('#text');
const deptSel = el('#dept');

function addMessage(role, content, meta) {
  const wrap = document.createElement('div');
  wrap.className = `msg ${role}`;
  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  if (role === 'bot' && typeof content === 'string' && content.trim().startsWith('<')) {
    bubble.innerHTML = content;
  } else {
    bubble.textContent = content;
  }
  wrap.appendChild(bubble);
  if (meta) {
    const metaEl = document.createElement('div');
    metaEl.className = 'meta';
    const badges = document.createElement('div');
    badges.className = 'badges';
    if (meta.dept) badges.innerHTML += `<span class="badge">Dept: ${meta.dept}</span>`;
    if (meta.action) badges.innerHTML += `<span class="badge">Action: ${meta.action}</span>`;
    if (meta.kag_hints && meta.kag_hints.length) badges.innerHTML += `<span class="badge">KAG: ${meta.kag_hints.join(' • ')}</span>`;
    metaEl.appendChild(badges);
    wrap.appendChild(metaEl);
  }
  messages.appendChild(wrap);
  messages.scrollTop = messages.scrollHeight;
}

function formatAction(data) {
  if (!data || !data.action) return null;
  if (data.action === 'hr_search_policies' && Array.isArray(data.result)) {
    const items = data.result.map(p => `<li><strong>${p.title}</strong><br/><span>${p.content}</span></li>`).join('');
    return `<div><div>Found ${data.result.length} policy matching your request:</div><ul>${items}</ul></div>`;
  }
  if (data.action === 'create_ticket' && data.result) {
    const t = data.result;
    return `<div>Ticket created: <strong>${t.ticket_id}</strong><br/>Priority: ${t.priority || 'n/a'}<br/>Status: ${t.status}</div>`;
  }
  if (data.action === 'reset_password' && data.result) {
    const r = data.result;
    return `<div>Password reset initiated for <strong>${r.user}</strong> (${r.status}).</div>`;
  }
  if (data.action === 'submit_claim' && data.result) {
    const c = data.result;
    return `<div>Claim submitted: <strong>${c.claim_id}</strong><br/>Status: ${c.status}</div>`;
  }
  return null;
}

async function send(text, dept) {
  addMessage('user', text);
  addMessage('bot', 'Thinking…');
  const sendBtn = document.querySelector('.composer button'); if (sendBtn) sendBtn.disabled = true;
  const res = await fetch('/chat', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, dept, conversation_id: conversationId })
  });
  const data = await res.json();
  // replace last bot message (Thinking…) with real content
  messages.removeChild(messages.lastChild);
  const pretty = data.answer || formatAction(data) || JSON.stringify(data);
  addMessage('bot', pretty, data);
  const sendBtn2 = document.querySelector('.composer button'); if (sendBtn2) sendBtn2.disabled = false;
  // feedback buttons
  const fb = document.createElement('div');
  fb.className = 'feedback';
  const up = document.createElement('button'); up.textContent = '👍';
  const down = document.createElement('button'); down.textContent = '👎';
  fb.appendChild(up); fb.appendChild(down);
  messages.lastChild.appendChild(fb);
  const submit = async (rating) => {
    await fetch('/feedback', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ trace_id: data.trace_id, text, dept: data.dept, answer: data.answer, rating, comment: '' }) });
    const ack = document.createElement('span'); ack.textContent = ' Thanks for your feedback!'; fb.appendChild(ack);
  };
  up.onclick = async () => { await submit('up'); up.disabled = true; down.disabled = true; };
  down.onclick = async () => { await submit('down'); up.disabled = true; down.disabled = true; };
}

const conversationId = crypto.randomUUID ? crypto.randomUUID() : (Date.now()+''+Math.random());

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  send(text, deptSel.value || null);
  input.value = '';
});
