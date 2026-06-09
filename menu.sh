#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate venv if present
if [[ -f "venv/bin/activate" ]]; then
    source venv/bin/activate
fi

menu() {
    echo ""
    echo "============================================================"
    echo "  STEPMANIA CHART GENERATOR - ArrowVortex Workflow"
    echo "============================================================"
    echo ""
    echo "  1. GENERATE FROM SM FILE"
    echo "     (Select an existing .sm + .mp3 to generate a full chart)"
    echo ""
    echo "  2. REGENERATE CHART (FAST)"
    echo "     (Reprocesses an existing chart using saved data)"
    echo ""
    echo "  3. CHANGE DIFFICULTY"
    echo "     (Increase/Decrease difficulty +/- 20% preserving Holds)"
    echo ""
    echo "  4. SUPPORT ME"
    echo "     (Support the project development)"
    echo ""
    echo "  9. Exit"
    echo ""
    echo "============================================================"
    echo ""
    read -rp "Select an option, or paste a YouTube URL: " choice

    if [[ "$choice" == *"http"* ]]; then
        echo ""
        echo "============================================================"
        echo "  YOUTUBE DOWNLOAD"
        echo "============================================================"
        echo ""
        python3 src/audioYouTube.py "$choice"
        read -rp "Press ENTER to continue..."
        menu
        return
    fi

    case "$choice" in
        1)
            echo ""
            echo "============================================================"
            echo "  1. GENERATE FROM SM FILE"
            echo "============================================================"
            echo ""
            python3 src/stepmania_generator.py
            read -rp "Press ENTER to continue..."
            menu
            ;;
        2)
            echo ""
            echo "============================================================"
            echo "  2. REGENERATE CHART (FAST)"
            echo "============================================================"
            echo ""
            python3 src/regenerate_menu.py
            read -rp "Press ENTER to continue..."
            menu
            ;;
        3)
            echo ""
            echo "============================================================"
            echo "  3. CHANGE DIFFICULTY"
            echo "============================================================"
            echo ""
            python3 src/modifica_steps.py
            read -rp "Press ENTER to continue..."
            menu
            ;;
        4)
            echo ""
            echo "============================================================"
            echo "  4. SUPPORT ME"
            echo "============================================================"
            echo ""
            python3 src/support_me.py
            menu
            ;;
        9)
            exit 0
            ;;
        *)
            echo ""
            echo "Invalid choice!"
            sleep 2
            menu
            ;;
    esac
}

menu
