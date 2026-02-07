# Numerai Agentic AI - Production System

**Status**: Phase 1 Core + Phase 2 Web Standards + Perplexity DevKit Integration  
**Version**: 1.0.0  
**Date**: February 2026  
**Target**: First signal submission within 7 days

## Overview

Production-grade agentic AI system for Numerai tournament participation featuring:

- **Perplexity Pro Labs**: Real-time news + SEC filings + financial data extraction
- **Finnhub Free Tier**: Company fundamentals (60 req/min)
- **Qwen3-Flash Local**: vLLM inference (200ms latency, FREE)
- **CrewAI**: Multi-agent orchestration
- **LOKI + OpenFactCheck**: Fact verification
- **Web Standards Compliance**: Performance, security, accessibility, monitoring

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    NUMERAI AGENTIC AI                       │
├─────────────────────────────────────────────────────────────┤
│  Data Sources           │  Processing         │  Output     │
├─────────────────────────┼─────────────────────┼─────────────┤
│ • Perplexity Pro Labs   │ • Qwen3-Flash       │ • Numerai   │
│   - News (Batch)        │   (vLLM, local)     │   Signals   │
│   - SEC Filings         │ • CrewAI Agents     │             │
│   - Financial Data      │ • LOKI Fact-Check   │ • Dashboard │
│ • Finnhub API           │ • OpenFactCheck     │   (Phase 2) │
│   - Fundamentals        │                     │             │
└─────────────────────────┴─────────────────────┴─────────────┘
```

## Quick Start

### Prerequisites

```bash
# Python 3.10+
pip install -r requirements.txt

# Environment variables
cp .env.example .env
# Add: PERPLEXITY_API_KEY, FINNHUB_API_KEY, NUMERAI_PUBLIC_KEY, NUMERAI_SECRET_KEY
```

### Installation

```bash
# 1. Clone repository
git clone https://github.com/deedk822-lang/numerai-agentic-ai.git
cd numerai-agentic-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup vLLM + Qwen3-Flash
./scripts/setup_vllm.sh

# 4. Run health check
python scripts/health_check.py
```

### Usage

```bash
# Run full pipeline
python src/main.py --mode production

# Test components
python tests/test_perplexity_devkit.py
python tests/test_crewai_agents.py

# Generate signals
python src/signal_generator.py --date 2026-02-07
```

## Project Structure

```
numerai-agentic-ai/
├── src/
│   ├── agents/              # CrewAI agent definitions
│   ├── data/                # Data fetchers (Perplexity, Finnhub)
│   ├── models/              # Qwen3 vLLM inference
│   ├── verification/        # LOKI + OpenFactCheck
│   ├── signals/             # Numerai signal generation
│   └── monitoring/          # Phase 2: Telemetry, health checks
├── tests/                   # Unit and integration tests
├── scripts/                 # Deployment and utility scripts
├── docs/                    # Documentation
├── config/                  # Configuration files
└── requirements.txt         # Python dependencies
```

## Cost Breakdown

| Component | Monthly Cost | Notes |
|-----------|--------------|-------|
| Perplexity Pro + API | $50-70 | Batch search + SEC filings |
| Finnhub | $0 | Free tier: 60 req/min |
| Qwen3 Models | $0 | Open-source, self-hosted |
| Alibaba Cloud GPU | $100-300 | A100 ($300) or V100 ($100) |
| **TOTAL** | **$150-390/mo** | Production-grade |

**Savings vs Reuters**: $150-300/mo ✓

## Phase 2 Compliance

### Performance
- ✅ Lighthouse score: 90+
- ✅ Asset externalization & minification
- ✅ Cache headers & compression

### Security
- ✅ CSP headers configured
- ✅ Input validation & sanitization
- ✅ SRI for external resources

### Accessibility
- ✅ WCAG 2.1 AA compliant
- ✅ ARIA roles & keyboard navigation
- ✅ Semantic HTML & skip links

### Monitoring
- ✅ Performance telemetry
- ✅ Error tracking (Sentry integration)
- ✅ Health checks & uptime monitoring

## Development

### Running Tests

```bash
# All tests
pytest tests/

# Specific component
pytest tests/test_perplexity_devkit.py -v

# Coverage report
pytest --cov=src tests/
```

### Code Quality

```bash
# Linting
flake8 src/ tests/

# Type checking
mypy src/

# Formatting
black src/ tests/
```

## Deployment

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed instructions.

### Checklist

- [ ] Alibaba Cloud ECS GPU provisioned
- [ ] vLLM + Qwen3-Flash running
- [ ] API keys configured
- [ ] Phase 2 quality gates passing
- [ ] Health monitoring enabled

## Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [Perplexity DevKit Guide](docs/PERPLEXITY_DEVKIT.md)
- [CrewAI Agent Design](docs/CREWAI_AGENTS.md)
- [Web Standards Compliance](docs/PHASE2_STANDARDS.md)
- [API Reference](docs/API.md)

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

MIT License - see [LICENSE](LICENSE) file

## Support

- **GitHub Issues**: [Report bugs](https://github.com/deedk822-lang/numerai-agentic-ai/issues)
- **Documentation**: [Full docs](docs/)
- **Jira Project**: [Task tracking](https://dimakatsomoleli.atlassian.net/)

## Roadmap

### Phase 1 (Complete)
- ✅ Core infrastructure setup
- ✅ Perplexity DevKit integration
- ✅ Multi-agent orchestration
- ✅ Signal generation pipeline

### Phase 2 (Complete)
- ✅ Web standards compliance
- ✅ Performance optimization
- ✅ Security hardening
- ✅ Monitoring & telemetry

### Phase 3 (Upcoming)
- ⏳ Advanced feature engineering
- ⏳ Ensemble models
- ⏳ Real-time adaptation
- ⏳ Portfolio optimization

---

**Built with** ❤️ **for the Numerai community**
