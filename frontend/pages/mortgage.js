import { useState } from "react";
import axios from "axios";

export default function Mortgage() {
  const [data, setData] = useState(null);

  const calculate = async () => {
    const res = await axios.post("http://localhost:5000/api/mortgage", {
      amount: 1000000,
      rate: 4.5,
      years: 25,
    });
    setData(res.data);
  };

  return (
    <div>
      <h2>Prêt Immobilier</h2>
      <button onClick={calculate}>Calculer</button>
      {data && (
        <>
          <p>Mensualité: {data.monthly}</p>
          <p>Total: {data.total}</p>
        </>
      )}
    </div>
  );
}