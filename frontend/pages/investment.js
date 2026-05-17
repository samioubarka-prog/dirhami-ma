import { useState } from "react";
import axios from "axios";

const API = process.env.NEXT_PUBLIC_API_URL;

export default function Investment() {
  const [result, setResult] = useState(null);

  const calculate = async () => {
    const res = await axios.post(API + "/api/investment", {
      initial: 10000,
      monthly: 500,
      rate: 6,
      years: 10,
    });

    setResult(res.data.futureValue);
  };

  return (
    <div>
      <h2>Simulateur Investissement</h2>
      <button onClick={calculate}>Calculer</button>
      {result && <p>Capital final: {result}</p>}
    </div>
  );
}