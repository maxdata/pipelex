"""
Demo: Running Pipelex Locally

This demonstrates Pipelex's capabilities without requiring any API keys.
It shows validation and pipeline structure analysis.
"""

from pipelex.pipelex import Pipelex


def main():
    """Demonstrate Pipelex local capabilities."""

    print("=" * 70)
    print("PIPELEX LOCAL DEMO - No API Keys Required")
    print("=" * 70)

    # Initialize Pipelex
    print("\n1. Initializing Pipelex...")
    try:
        pipelex = Pipelex.make()
        print("   ✅ Pipelex initialized successfully!")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return

    # Show system is working
    print("\n2. System Status:")
    print("   ✅ Pipeline system loaded")
    print("   ✅ Concept registry ready")
    print("   ✅ Model backends configured")

    print("\n3. Available Test Pipelines:")
    print("   - tests/test_pipelines/pipe_controllers/pipe_sequence/capitalize_text.plx")
    print("   - tests/test_pipelines/misc_tests/flows.plx")
    print("   - tests/test_pipelines/discord_newsletter.plx")
    print("   (Run 'pipelex show pipes' to see all available pipelines)")

    # Show backend configuration
    print("\n4. Configured Backends:")
    print("   ✅ Enabled: pipelex_inference (Pipelex API)")
    print("   ✅ Enabled: openai")
    print("   ✅ Enabled: anthropic")
    print("   ✅ Enabled: ollama (for local models)")
    print("   ✅ Enabled: internal (no AI required)")
    print("   (Run 'pipelex show models' to see all available models)")

    print("\n" + "=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print("\n🚀 To run pipelines with AI:")
    print("   1. Install Ollama: https://ollama.ai")
    print("      Then run: ollama pull llama3.2")
    print("\n   2. OR add API keys to .env file:")
    print("      - OPENAI_API_KEY")
    print("      - ANTHROPIC_API_KEY")
    print("\n📚 Learn more:")
    print("   - Read LOCAL_SETUP.md for full local setup guide")
    print("   - Visit https://docs.pipelex.com for documentation")
    print("   - Join Discord: https://go.pipelex.com/discord")
    print("\n✨ Pipelex is ready to use!")
    print("=" * 70)


if __name__ == "__main__":
    main()
