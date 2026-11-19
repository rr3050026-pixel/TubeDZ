/**
 * TubeDZ Desktop Core Engine — Content Script
 * 100% Ad-Free, Auto-Skip, AMOLED Black Theme, Background Audio
 * Project: « وزارة المساكين » 🇩🇿
 */

(function() {
    'use strict';

    console.log('[TubeDZ Desktop] Core Engine Initialized 🇩🇿');

    // 1. FAST VIDEO AD SKIPPER
    function handleVideoAds() {
        const moviePlayer = document.querySelector('#movie_player');
        const video = document.querySelector('video');

        if (moviePlayer && moviePlayer.classList.contains('ad-showing')) {
            if (video && !isNaN(video.duration) && isFinite(video.duration)) {
                try {
                    video.muted = true;
                    video.playbackRate = 16.0;
                    video.currentTime = video.duration;
                } catch (e) {}
            }

            // Click all possible skip buttons
            const skipButtons = document.querySelectorAll(
                '.ytp-ad-skip-button, .ytp-ad-skip-button-modern, .ytp-skip-ad-button, .ytp-ad-skip-button-slot button, .ytp-ad-overlay-close-button'
            );
            skipButtons.forEach(btn => {
                try { btn.click(); } catch (e) {}
            });
        }

        // Auto-dismiss anti-adblock dialog if appears
        const antiAdblockDialog = document.querySelector('ytd-enforcement-message-view-model, tp-yt-paper-dialog[aria-modal="true"]');
        if (antiAdblockDialog) {
            antiAdblockDialog.remove();
            const backdrop = document.querySelector('tp-yt-iron-overlay-backdrop');
            if (backdrop) backdrop.remove();
            if (video && video.paused) {
                video.play();
            }
        }
    }

    // Run ad skipper on high frequency
    setInterval(handleVideoAds, 100);

    // 2. TUBE DZ HEADER BRANDING
    function injectTubeDZBadge() {
        const logoContainer = document.querySelector('ytd-topbar-logo-renderer #logo');
        if (logoContainer && !document.querySelector('#tubedz-badge')) {
            const badge = document.createElement('span');
            badge.id = 'tubedz-badge';
            badge.innerHTML = `
                <span style="
                    display: inline-flex;
                    align-items: center;
                    gap: 6px;
                    background: linear-gradient(135deg, rgba(0, 200, 83, 0.2), rgba(239, 68, 68, 0.2));
                    border: 1px solid rgba(74, 222, 128, 0.4);
                    padding: 3px 10px;
                    border-radius: 12px;
                    margin-left: 12px;
                    font-size: 11px;
                    font-weight: 800;
                    color: #4ade80;
                    font-family: system-ui, sans-serif;
                ">
                    🇩🇿 TubeDZ • وزارة المساكين
                </span>
            `;
            logoContainer.parentNode.insertBefore(badge, logoContainer.nextSibling);
        }
    }

    // 3. BACKGROUND PLAY ENABLER (Prevent pause on blur)
    function enableBackgroundPlay() {
        Object.defineProperty(document, 'hidden', {
            get: () => false,
            configurable: true
        });
        Object.defineProperty(document, 'visibilityState', {
            get: () => 'visible',
            configurable: true
        });
        document.dispatchEvent(new Event('visibilitychange'));
    }

    window.addEventListener('DOMContentLoaded', () => {
        enableBackgroundPlay();
        injectTubeDZBadge();
        setInterval(injectTubeDZBadge, 2000);
    });

})();
