const express = require("express");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

app.get("/", (req,res)=> res.send("API running"));

app.post("/api/investment", (req, res) => {
  const { initial, monthly, rate, years } = req.body;
  const r = rate / 100 / 12;
  const n = years * 12;

  let futureValue =
    initial * Math.pow(1 + r, n) +
    monthly * ((Math.pow(1 + r, n) - 1) / r);

  res.json({ futureValue: futureValue.toFixed(2) });
});

app.post("/api/mortgage", (req, res) => {
  const { amount, rate, years } = req.body;

  const r = rate / 100 / 12;
  const n = years * 12;

  const monthly = (amount * r) / (1 - Math.pow(1 + r, -n));
  const total = monthly * n;

  res.json({
    monthly: monthly.toFixed(2),
    total: total.toFixed(2),
  });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log("Server running on " + PORT));