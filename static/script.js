document.addEventListener('DOMContentLoaded', () => {
    const tbody = document.getElementById('jogadores-tbody');
    const form = document.getElementById('add-jogador-form');
    const btnOrdenar = document.getElementById('btn-ordenar');
    const btnRandomizar = document.getElementById('btn-randomizar');
    const btnBuscar = document.getElementById('btn-buscar');
    const btnLimparBusca = document.getElementById('btn-limpar-busca');
    const inputBusca = document.getElementById('busca-nome');
    const feedback = document.getElementById('form-feedback');
    const tempoContainer = document.getElementById('tempo-container');

    async function carregarJogadores() {
        try {
            const response = await fetch('/api/jogadores');
            const data = await response.json();
            renderizarTabela(data);
            tempoContainer.textContent = ''; 
        } catch (error) {
            console.error('Erro ao carregar jogadores:', error);
            mostrarFeedback('Erro ao carregar lista de jogadores.', 'error');
        }
    }

    function renderizarTabela(jogadores) {
        tbody.innerHTML = '';
        
        if (jogadores.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align: center;">Nenhum jogador encontrado.</td></tr>';
            return;
        }

        jogadores.forEach(jogador => {
            const tr = document.createElement('tr');
            
            const statusClass = jogador.pago ? 'status-paid' : 'status-unpaid';
            const statusText = jogador.pago ? 'Pago' : 'Deve';

            tr.innerHTML = `
                <td>${jogador.nome}</td>
                <td>${jogador.posicao}</td>
                <td><span class="status-badge ${statusClass}">${statusText}</span></td>
                <td>
                    <button class="btn-pagamento btn-secondary" data-nome="${jogador.nome}" style="padding: 0.25rem 0.5rem; font-size: 0.85rem;">
                        Alterar Status
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });

        // Adicionar eventos aos botões de pagamento
        document.querySelectorAll('.btn-pagamento').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const nome = e.target.getAttribute('data-nome');
                await alterarPagamento(nome);
            });
        });
    }

    async function alterarPagamento(nome) {
        try {
            const response = await fetch(`/api/jogadores/${encodeURIComponent(nome)}/pagamento`, {
                method: 'PUT'
            });
            if (response.ok) {
                // Se estivermos em uma busca, recarrega a busca. Se não, recarrega a lista toda.
                if (inputBusca.value.trim() !== '') {
                    btnBuscar.click();
                } else {
                    carregarJogadores();
                }
            } else {
                alert('Erro ao alterar status de pagamento.');
            }
        } catch (error) {
            console.error('Erro:', error);
            alert('Erro na comunicação com o servidor.');
        }
    }

    // submeter formulário
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const nome = document.getElementById('nome').value.trim();
        const posicao = document.getElementById('posicao').value;
        const pago = document.getElementById('pago').checked;

        try {
            const response = await fetch('/api/jogadores', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ nome, posicao, pago })
            });

            const data = await response.json();

            if (response.ok) {
                mostrarFeedback(data.message, 'success');
                form.reset();
                carregarJogadores(); 
            } else {
                mostrarFeedback(data.detail, 'error');
            }
        } catch (error) {
            console.error('Erro ao adicionar jogador:', error);
            mostrarFeedback('Erro de conexão com o servidor.', 'error');
        }
    });

    // randomizar lista
    btnRandomizar.addEventListener('click', async () => {
        btnRandomizar.disabled = true;
        btnRandomizar.textContent = 'Randomizando...';

        try {
            const response = await fetch('/api/jogadores/randomizar', { method: 'POST' });
            
            if (response.ok) {
                const data = await response.json();
                renderizarTabela(data.jogadores);
                tempoContainer.textContent = 'A lista em memória foi randomizada! (JSON não foi alterado)';
                
                const table = document.getElementById('jogadores-table');
                table.style.opacity = '0.5';
                setTimeout(() => table.style.opacity = '1', 200);
            } else {
                alert('Erro ao randomizar a lista.');
            }
        } catch (error) {
            console.error('Erro ao randomizar:', error);
            alert('Erro ao comunicar com o servidor.');
        } finally {
            btnRandomizar.disabled = false;
            btnRandomizar.textContent = '🔀 Randomizar';
        }
    });

    // ordenar jogadores
    btnOrdenar.addEventListener('click', async () => {
        const criterio = document.getElementById('criterio').value;
        const algoritmo = document.getElementById('algoritmo').value;

        btnOrdenar.disabled = true;
        btnOrdenar.textContent = 'Ordenando...';

        try {
            const response = await fetch(`/api/jogadores/ordenar?criterio=${criterio}&algoritmo=${algoritmo}`);
            
            if (response.ok) {
                const data = await response.json(); 
                renderizarTabela(data.jogadores);
                
                tempoContainer.textContent = `⏱️ Tempo de ordenação (${algoritmo}): ${data.tempo_ms.toFixed(4)} ms`;
                
                const table = document.getElementById('jogadores-table');
                table.style.opacity = '0.5';
                setTimeout(() => table.style.opacity = '1', 200);
            } else {
                const data = await response.json();
                alert(`Erro: ${data.detail}`);
            }
        } catch (error) {
            console.error('Erro ao ordenar:', error);
            alert('Erro ao comunicar com o servidor para ordenação.');
        } finally {
            btnOrdenar.disabled = false;
            btnOrdenar.textContent = 'Ordenar Lista';
        }
    });

    // buscar jogador
    btnBuscar.addEventListener('click', async () => {
        const nome = inputBusca.value.trim();
        if (!nome) return;

        try {
            const response = await fetch(`/api/jogadores/buscar?nome=${encodeURIComponent(nome)}`);
            if (response.ok) {
                const data = await response.json();
                renderizarTabela(data);
                btnLimparBusca.style.display = 'block';
                tempoContainer.textContent = `Resultados da busca para: "${nome}"`;
            }
        } catch (error) {
            console.error('Erro ao buscar:', error);
        }
    });

    btnLimparBusca.addEventListener('click', () => {
        inputBusca.value = '';
        btnLimparBusca.style.display = 'none';
        carregarJogadores();
    });

    carregarJogadores();
});
