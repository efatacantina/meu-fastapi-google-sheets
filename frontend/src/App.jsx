import { useState } from "react";

function App() {
  const [produto, setProduto] = useState("");
  const [quantidade, setQuantidade] = useState(1);
  const [preco, setPreco] = useState(0);

  const enviar = async () => {
    const resposta = await fetch("http://localhost:8000/registrar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ produto, quantidade, preco }),
    });

    const dados = await resposta.json();
    alert("Registro enviado!");
    console.log(dados);
  };

  return (
    <div style={{ padding: "40px" }}>
      <h1>Registro de Venda</h1>

      <input 
        placeholder="Produto" 
        value={produto} 
        onChange={e => setProduto(e.target.value)} 
      />
      <br />

      <input 
        type="number"
        placeholder="Quantidade" 
        value={quantidade} 
        onChange={e => setQuantidade(+e.target.value)} 
      />
      <br />

      <input 
        type="number"
        placeholder="Preço" 
        value={preco} 
        onChange={e => setPreco(+e.target.value)} 
      />
      <br /><br />

      <button onClick={enviar}>Salvar</button>
    </div>
  );
}

export default App;
