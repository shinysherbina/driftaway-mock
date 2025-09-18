import express from "express";
import cors from "cors";
import snipSmart from "./snipSmart.js";
import snipJson from "./snipJson.js";

const app = express();
const port = process.env.PORT || 3000;

// Enable CORS for all routes
app.use(cors());
app.use(express.json());

/**
 * Health check endpoint
 */
app.get("/health", (req, res) => {
  res.status(200).json({ status: "ok" });
});

/**
 * POST /clean
 * Cleans an AI-generated response using snipSmart.
 *
 * Request body:
 * {
 *   "text": "<raw AI response>",
 *   "format": "json" // or "html", "xml", etc.
 * }
 *
 * Response:
 * {
 *   "data": "<cleaned text>",
 *   "meta": { ...optional metadata... }
 * }
 */
app.post("/clean", (req, res) => {
  const { text, format } = req.body;

  if (!text) {
    return res.status(400).json({ error: 'The "text" field is required.' });
  }

  const options = format ? { format: format } : { format: "json" };
  const result = snipSmart(text, options);

  if (result.data === null) {
    return res.status(400).json({
      error: "Failed to clean the input text. See details in the result.",
      result,
    });
  }

  res.status(200).json({
    data: result.data,
    meta: {
      status: result.status,
      comments: result.comments,
    },
  });
});

// POST /snip-json
// Directly invokes snipJson without going through snipSmart
app.post("/snip-json", (req, res) => {
  const { text } = req.body;

  if (!text) {
    return res.status(400).json({ error: 'The "text" field is required.' });
  }

  try {
    const result = snipJson(text);

    if (result.data === null) {
      return res.status(400).json({
        error: "snipJson returned null data.",
        result,
      });
    }

    res.status(200).json({
      data: result.data,
      meta: {
        status: result.status || "ok",
        comments: result.comments || "Processed via snipJson",
      },
    });
  } catch (err) {
    res.status(500).json({
      error: "Internal error while processing snipJson.",
      details: err.message,
    });
  }
});

app.listen(port, () => {
  console.log(`snipSmart server listening at http://localhost:${port}`);
});
