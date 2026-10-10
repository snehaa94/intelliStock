document.addEventListener('DOMContentLoaded', () => {
  const canvas = document.getElementById('salesChart');
  if (canvas && window.Chart) {
    try { const data = JSON.parse(canvas.dataset.chart || '{}'); new Chart(canvas, {type:'line',data:{labels:data.labels||[],datasets:[{label:'Units sold',data:data.units||[],borderColor:'#3157d5',backgroundColor:'rgba(49,87,213,.10)',fill:true,tension:.28,pointRadius:2}]},options:{responsive:true,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true,ticks:{precision:0}},x:{grid:{display:false}}}}}); } catch(e) { console.error('Chart data could not be rendered.'); }
  }
  const forecastButton = document.getElementById('runForecast');
  if (forecastButton) forecastButton.addEventListener('click', async () => {
    const id = document.getElementById('forecastProduct').value;
    const days = document.getElementById('forecastDays').value;
    const target = document.getElementById('forecastResult');
    if (!id) return;
    forecastButton.disabled = true; forecastButton.textContent = 'Calculating…';
    try { const r = await fetch(`/api/forecast/${encodeURIComponent(id)}/?days=${encodeURIComponent(days)}`); const d = await r.json(); if (!r.ok) throw new Error(d.error || 'Forecast failed');
      target.innerHTML = `<section class="panel"><div class="row g-3 mb-3"><div class="col-md-4"><div class="metric"><div class="metric-label">Predicted units</div><div class="metric-value">${Number(d.total_forecast).toLocaleString()}</div></div></div><div class="col-md-4"><div class="metric"><div class="metric-label">Suggested replenishment</div><div class="metric-value">${Number(d.recommendation).toLocaleString()}</div></div></div><div class="col-md-4"><div class="metric"><div class="metric-label">Evaluation MAE</div><div class="metric-value">${d.mae === null ? 'N/A' : Number(d.mae).toFixed(2)}</div></div></div></div><h2 class="h5">${escapeHtml(d.product)} <span class="text-secondary small">(${escapeHtml(d.sku)})</span></h2><p class="text-secondary small">Method: ${escapeHtml(d.method)}</p><canvas id="forecastChart" height="100"></canvas><p class="small text-secondary mt-3">${escapeHtml(d.note)}</p></section>`;
      const c = document.getElementById('forecastChart'); new Chart(c,{type:'bar',data:{labels:d.daily_forecast.map((_,i)=>`Day ${i+1}`),datasets:[{label:'Forecast units',data:d.daily_forecast,backgroundColor:'#8ba4ff',borderRadius:6}]},options:{responsive:true,plugins:{legend:{display:false}},scales:{y:{beginAtZero:true}}}});
    } catch(e) { target.innerHTML = `<div class="alert alert-warning">${escapeHtml(e.message)}</div>`; } finally { forecastButton.disabled = false; forecastButton.textContent = 'Generate forecast'; }
  });
  const form = document.getElementById('assistantForm');
  if (form) form.addEventListener('submit', async (event) => {
    event.preventDefault(); const input = document.getElementById('question'); const log = document.getElementById('chatLog'); const status = document.getElementById('assistantStatus'); const question = input.value.trim(); if (!question) return;
    addBubble(log, question, 'user'); input.value=''; status.textContent='Thinking…';
    const csrf = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    try { const response = await fetch(form.dataset.endpoint,{method:'POST',headers:{'Content-Type':'application/json','X-CSRFToken':csrf||''},body:JSON.stringify({question})}); const data=await response.json(); if(!response.ok) throw new Error(data.error||'Request failed'); addBubble(log, `${data.answer}

Mode: ${data.mode}`, 'assistant'); status.textContent=''; }
    catch(e){addBubble(log,e.message,'assistant');status.textContent='';}
  });
});
function addBubble(log,text,kind){const el=document.createElement('div');el.className=`chat-bubble ${kind}`;el.textContent=text;log.appendChild(el);log.scrollTop=log.scrollHeight;}
function escapeHtml(value){return String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
