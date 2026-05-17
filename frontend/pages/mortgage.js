import { useState } from "react";
import axios from "axios";

const API = process.env.NEXT_PUBLIC_API_URL;

export default function Mortgage() {
  const [data, setData] = useState(null);

  const calculate = async () => {
    const res = await axios.post(API + "/api/mortgage", {
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