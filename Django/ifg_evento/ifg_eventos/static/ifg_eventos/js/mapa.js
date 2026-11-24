const modalMapa = document.getElementById("modal-mapa");

const botaoAbrirMapa = document.getElementById("abrir-mapa");
const botaoFecharMapa = document.getElementById("fechar-mapa");
const botaoCancelarMapa = document.getElementById("cancelar-mapa");
const botaoConfirmarMapa = document.getElementById("confirmar-mapa");

const campoLocal = document.getElementById("local");
const campoLatitude = document.getElementById("latitude");
const campoLongitude = document.getElementById("longitude");

let mapa = null;
let marcador = null;
let localizacaoSelecionada = null;

// Inicializa o mapa
function inicializarMapa() {
    if (mapa !== null) {
        mapa.invalidateSize();
        return;
    }

    // Garante que o ícone do pino azul carregue corretamente
    delete L.Icon.Default.prototype._getIconUrl;
    L.Icon.Default.mergeOptions({
        iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
        iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
        shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
    });

    // Centro inicial do mapa: Goiânia / IFG
    mapa = L.map("mapa").setView([-16.68, -49.25], 13);

    //
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(mapa);

    // Evento executado quando o usuário clica no mapa
    mapa.on("click", function(evento) {
        selecionarLocalizacao(evento.latlng);
    });
}

// Seleciona uma localização
function selecionarLocalizacao(coordenadas) {
    const latitude = coordenadas.lat;
    const longitude = coordenadas.lng;

    localizacaoSelecionada = {
        latitude: latitude,
        longitude: longitude
    };

    if (marcador === null) {
        marcador = L.marker(coordenadas, {
            draggable: true
        }).addTo(mapa);

        // Permite arrastar o marcador
        marcador.on("dragend", function(evento) {
            const novaPosicao = evento.target.getLatLng();
            selecionarLocalizacao(novaPosicao);
        });

    } else {
        marcador.setLatLng(coordenadas);
    }

    botaoConfirmarMapa.disabled = false;
}


function abrirMapa() {
    modalMapa.classList.add("aberto");

    inicializarMapa();

    setTimeout(function() {
        mapa.invalidateSize();
    }, 100);
}

function fecharMapa() {
    modalMapa.classList.remove("aberto");
}

// Confirma a localização selecionada e busca seu endereço.
async function confirmarLocalizacao() {
    if (localizacaoSelecionada === null) {
        return;
    }

    const localizacao = localizacaoSelecionada;
    const { latitude, longitude } = localizacao;
    const textoBotao = botaoConfirmarMapa.textContent;
    const parametros = new URLSearchParams({
        lat: String(latitude),
        lon: String(longitude),
        format: "jsonv2",
        addressdetails: "1",
        "accept-language": "pt-BR"
    });

    botaoConfirmarMapa.disabled = true;
    botaoConfirmarMapa.textContent = "Buscando endereço...";

    try {
        const resposta = await fetch(
            `https://nominatim.openstreetmap.org/reverse?${parametros}`
        );

        if (!resposta.ok) {
            throw new Error(`Consulta de endereço falhou: HTTP ${resposta.status}`);
        }

        const resultado = await resposta.json();
        const endereco = resultado.address || {};
        const partesEndereco = [
            [endereco.road, endereco.house_number].filter(Boolean).join(", "),
            endereco.neighbourhood || endereco.suburb || endereco.city_district,
            endereco.city || endereco.town || endereco.village || endereco.municipality,
            endereco.state,
            endereco.postcode
        ].filter(Boolean);
        const enderecoLegivel = partesEndereco.join(", ") || resultado.display_name;

        if (typeof enderecoLegivel !== "string" || !enderecoLegivel.trim()) {
            throw new Error("Nenhum endereço foi encontrado para essas coordenadas.");
        }

        if (
            localizacaoSelecionada !== localizacao ||
            !modalMapa.classList.contains("aberto")
        ) {
            return;
        }

        campoLatitude.value = latitude;
        campoLongitude.value = longitude;
        campoLocal.value = enderecoLegivel.slice(0, 255);
        fecharMapa();
    } catch (erro) {
        console.error("Não foi possível buscar o endereço da localização.", erro);
        alert("Não foi possível obter o endereço. Verifique a conexão e tente novamente.");
    } finally {
        botaoConfirmarMapa.disabled = localizacaoSelecionada === null;
        botaoConfirmarMapa.textContent = textoBotao;
    }
}

// Eventos dos botões
botaoAbrirMapa.addEventListener("click", abrirMapa);
botaoFecharMapa.addEventListener("click", fecharMapa);
botaoCancelarMapa.addEventListener("click", fecharMapa);
botaoConfirmarMapa.addEventListener("click", confirmarLocalizacao);

// Fecha ao clicar fora da janela
modalMapa.addEventListener("click", function(evento) {
    if (evento.target === modalMapa) {
        fecharMapa();
    }
});
