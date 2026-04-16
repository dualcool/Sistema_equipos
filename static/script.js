let editando = null;

const departamentos = {
    "Sistemas": ["Soporte", "Desarrollo", "Redes"],
    "Administración": ["Contabilidad", "Talento Humano"],
    "Finanzas": ["Tesorería", "Presupuesto"],
    "Secretaría": ["Archivo", "Recepción"]
};

const selectDepto = document.getElementById("departamento");
const selectOficina = document.getElementById("oficina");
const selectTipo = document.querySelector('[name="tipo"]');

const camposPC = [
    document.querySelector('[name="cpu"]').parentElement,
    document.querySelector('[name="ram"]').parentElement
];

// ocultar campos
function actualizarCamposPorTipo(tipo) {
    if (tipo === 'Impresora' || tipo === 'Router') {
        camposPC.forEach(c => c.style.display = 'none');
    } else {
        camposPC.forEach(c => c.style.display = 'block');
    }
}

selectTipo.addEventListener('change', () => {
    actualizarCamposPorTipo(selectTipo.value);
});

// departamentos
for (let depto in departamentos) {
    let option = document.createElement("option");
    option.value = depto;
    option.textContent = depto;
    selectDepto.appendChild(option);
}

selectDepto.addEventListener("change", () => {
    const oficinas = departamentos[selectDepto.value] || [];
    selectOficina.innerHTML = '<option value="">Seleccione</option>';

    oficinas.forEach(of => {
        let option = document.createElement("option");
        option.value = of;
        option.textContent = of;
        selectOficina.appendChild(option);
    });
});

// buscador
document.getElementById("buscador").addEventListener("keyup", function () {
    let filtro = this.value.toLowerCase();
    document.querySelectorAll("tbody tr").forEach(fila => {
        fila.style.display = fila.innerText.toLowerCase().includes(filtro) ? "" : "none";
    });
});

// contador
function contarEstados() {
    let b=0,r=0,m=0;
    document.querySelectorAll("tbody tr").forEach(f => {
        let t=f.children[8].innerText;
        if(t.includes("Bueno")) b++;
        else if(t.includes("Regular")) r++;
        else m++;
    });
    document.getElementById("buenos").textContent=b;
    document.getElementById("regulares").textContent=r;
    document.getElementById("malos").textContent=m;
}
window.onload=contarEstados;

// mensajes
function mostrarMensaje(texto,tipo){
    const d=document.createElement("div");
    d.className=`alert alert-${tipo} position-fixed top-0 end-0 m-3`;
    d.textContent=texto;
    document.body.appendChild(d);
    setTimeout(()=>d.remove(),2000);
}

// guardar
document.getElementById('formEquipo').onsubmit = async e => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.target));

    if (!data.nombre || !data.numero_serie) {
        mostrarMensaje("Campos obligatorios", "danger");
        return;
    }

    const url = editando ? `/api/equipo/${editando}` : '/api/equipo';
    const method = editando ? 'PUT' : 'POST';

    const res = await fetch(url,{
        method,
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify(data)
    });

    const result = await res.json();

    if(result.success){
        mostrarMensaje("Guardado correctamente","success");
        setTimeout(()=>location.reload(),1000);
    }
};

// editar
async function editar(id){
    const res=await fetch(`/api/equipo/${id}`);
    const equipo=await res.json();

    editando=equipo.id;

    for (let [k,v] of Object.entries(equipo)) {
        let input=document.querySelector(`[name="${k}"]`);
        if(input && k!=="departamento" && k!=="oficina"){
            input.value=v||'';
        }
    }

    selectDepto.value=equipo.departamento;
    selectDepto.dispatchEvent(new Event('change'));
    setTimeout(()=>selectOficina.value=equipo.oficina,100);

    selectTipo.value=equipo.tipo;
    actualizarCamposPorTipo(equipo.tipo);

    new bootstrap.Modal(document.getElementById('modalEquipo')).show();
}

// borrar
async function borrar(id){
    if(confirm("¿Eliminar?")){
        await fetch(`/api/equipo/${id}`,{method:'DELETE'});
        location.reload();
    }
}

// reset
document.getElementById('modalEquipo').addEventListener('hidden.bs.modal',()=>{
    document.getElementById('formEquipo').reset();
    editando=null;
    actualizarCamposPorTipo('Escritorio');
});