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

    // 4. SMART TV CAST ENABLER
    function injectCastButton() {
        const rightControls = document.querySelector('.ytp-right-controls');
        if (rightControls && !document.querySelector('#tubedz-cast-btn')) {
            const castBtn = document.createElement('button');
            castBtn.id = 'tubedz-cast-btn';
            castBtn.className = 'ytp-button';
            castBtn.title = 'TubeDZ Cast: البث إلى التلفزيون الذكي (Smart TV)';
            castBtn.setAttribute('aria-label', 'البث على التلفزيون الذكي');
            castBtn.innerHTML = `
                <svg height="100%" version="1.1" viewBox="0 0 36 36" width="100%" style="vertical-align: middle;">
                    <path d="M4,24 L4,26 C6.76,26 9,28.24 9,31 L11,31 C11,27.13 7.87,24 4,24 Z M4,20 L4,22 C8.97,22 13,26.03 13,31 L15,31 C15,24.92 10.08,20 4,20 Z M4,16 L4,18 C11.18,18 17,23.82 17,31 L19,31 C19,22.72 12.28,16 4,16 Z M28,8 L8,8 C6.9,8 6,8.9 6,10 L6,14 L8,14 L8,10 L28,10 L28,26 L20,26 L20,28 L28,28 C29.1,28 30,27.1 30,26 L30,10 C30,8.9 29.1,8 28,8 Z" fill="#4ade80"></path>
                </svg>
            `;
            castBtn.onclick = () => {
                const video = document.querySelector('video');
                if (video && video.remote && typeof video.remote.prompt === 'function') {
                    video.remote.prompt().catch(() => {
                        window.open('https://www.youtube.com/pair', '_blank');
                    });
                } else {
                    window.open('https://www.youtube.com/pair', '_blank');
                }
            };
            rightControls.insertBefore(castBtn, rightControls.firstChild);
        }
    }

    window.addEventListener('DOMContentLoaded', () => {
        enableBackgroundPlay();
        injectTubeDZBadge();
        injectCastButton();
        setInterval(injectTubeDZBadge, 2000);
        setInterval(injectCastButton, 1500);
    });

})();
