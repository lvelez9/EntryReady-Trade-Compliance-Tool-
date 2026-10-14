# OriginDocs

**Supplier-side HS classification check for US imports.**

Foreign suppliers often send shipment data with vague product descriptions and generic or wrong HS codes. Those errors travel down the chain to the freight forwarder, customs broker and US importer, where they show up as duty overpayment, customs holds and compliance exposure.

OriginDocs captures shipment data at the source and reviews it the way a customs broker would, before the goods move.

Built through Georgia Tech's CREATE-X Idea to Prototype program.

## What it does

1. The supplier fills in seven broker-critical fields: supplier identity, country of origin, Incoterms, item description and material, quantity and weights, valuation, and their suggested HS code.
2. The data is sent to Claude, prompted as a licensed US customs broker.
3. The tool returns a classification memo with:
   - a suggested HTSUS code and GRI-based rationale
   - an assessment of the supplier's own code
   - regulatory flags: Section 301, UFLPA, AD/CVD and PGA requirements
   - questions to send back to the supplier to reach a full 10-digit code
   - CBP precedent references
4. Results export to CSV or JSON.

## Run it locally

You need Python 3 and an [Anthropic API key](https://console.anthropic.com).

1. Set your API key once (macOS / zsh):

   ```bash
   echo 'export ANTHROPIC_API_KEY="your-key-here"' >> ~/.zshrc
   ```

   Then open a new Terminal window.

2. Start the server from this folder:

   ```bash
   python3 server.py
   ```

3. Open <http://localhost:8080/origindocs.html>.

## How it's built

- **`origindocs.html`**: the intake form and memo display (HTML/JS).
- **`server.py`**: a small Python proxy server. It forwards requests to the Anthropic API from the server side, which avoids browser CORS restrictions and keeps the API key out of the browser. The key is read from the `ANTHROPIC_API_KEY` environment variable and is never stored in the code.

## Limitations

This is a prototype. Classifications come from a general-purpose model. It isn't fine-tuned and isn't connected to CBP's CROSS rulings database, so cited rulings should be verified. It doesn't replace a licensed customs broker.
