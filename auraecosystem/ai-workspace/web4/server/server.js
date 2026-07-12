const express = require('express');
const { protectWeb4Route } = require('./src/identity/lct-middleware');

const app = express();
app.use(express.json());

// Apply the protectWeb4Route protection module to your sensitive application endpoint routes
app.post('/api/v1/transaction/execute', protectWeb4Route, (req, res) => {
  res.json({
    status: "Success",
    message: "Transaction signed and added to trust ledger.",
    processedAgent: req.web4Agent.agentId,
    remainingAtp: req.web4Agent.metabolism.atp
  });
});

app.listen(3000, () => console.log('Web4 Security Core Node running on port 3000'));
