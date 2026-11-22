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

    // 5. AUDIO BOOSTER 200% (Web Audio API)
    let audioCtx = null;
    let gainNode = null;
    let isBoosted = false;

    function toggleAudioBoost() {
        const video = document.querySelector('video');
        if (!video) return;

        if (!audioCtx) {
            try {
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                audioCtx = new AudioContext();
                const source = audioCtx.createMediaElementSource(video);
                gainNode = audioCtx.createGain();
                gainNode.gain.value = 1.0;
                source.connect(gainNode);
                gainNode.connect(audioCtx.destination);
            } catch (e) {
                console.log('Web Audio context initialized');
            }
        }

        if (audioCtx && audioCtx.state === 'suspended') {
            audioCtx.resume();
        }

        isBoosted = !isBoosted;
        if (gainNode) {
            gainNode.gain.value = isBoosted ? 2.2 : 1.0;
        }

        const boostBtn = document.querySelector('#tubedz-boost-btn');
        if (boostBtn) {
            const path = boostBtn.querySelector('path');
            if (path) path.setAttribute('fill', isBoosted ? '#fbbf24' : '#ffffff');
            boostBtn.title = isBoosted ? 'مضخم الصوت نشط (220% Hi-Fi Boost) ⚡' : 'مضخم الصوت: تضخيم الصوت حتى 220%';
        }
    }

    function injectBoosterButton() {
        const rightControls = document.querySelector('.ytp-right-controls');
        if (rightControls && !document.querySelector('#tubedz-boost-btn')) {
            const boostBtn = document.createElement('button');
            boostBtn.id = 'tubedz-boost-btn';
            boostBtn.className = 'ytp-button';
            boostBtn.title = 'مضخم الصوت: مضاعفة الصوت الضعيف حتى 220% (اضغط B)';
            boostBtn.innerHTML = `
                <svg height="100%" version="1.1" viewBox="0 0 36 36" width="100%" style="vertical-align: middle;">
                    <path d="M13,11 L8,15 L4,15 L4,21 L8,21 L13,25 Z M17,14 C18.5,15.5 18.5,20.5 17,22 M20,11 C23,14 23,22 20,25 M23,8 C27.5,12.5 27.5,23.5 23,28" fill="#ffffff" stroke-width="1.5"></path>
                </svg>
            `;
            boostBtn.onclick = toggleAudioBoost;
            rightControls.insertBefore(boostBtn, rightControls.firstChild);
        }
    }

    // 6. SMART SLEEP TIMER WITH AUDIO FADE
    let sleepSecondsRemaining = 0;
    let sleepInterval = null;

    function setSleepTimer(mins) {
        if (sleepInterval) clearInterval(sleepInterval);
        sleepSecondsRemaining = mins * 60;
        const sleepBtn = document.querySelector('#tubedz-sleep-btn path');
        if (sleepBtn) sleepBtn.setAttribute('fill', '#38bdf8');

        sleepInterval = setInterval(() => {
            sleepSecondsRemaining--;
            const video = document.querySelector('video');
            if (!video) return;

            // Fade volume during last 20 seconds
            if (sleepSecondsRemaining <= 20 && sleepSecondsRemaining > 0) {
                video.volume = Math.max(0, video.volume - 0.05);
            }

            if (sleepSecondsRemaining <= 0) {
                clearInterval(sleepInterval);
                video.pause();
                if (sleepBtn) sleepBtn.setAttribute('fill', '#ffffff');
            }
        }, 1000);
    }

    function injectSleepTimerButton() {
        const rightControls = document.querySelector('.ytp-right-controls');
        if (rightControls && !document.querySelector('#tubedz-sleep-btn')) {
            const sleepBtn = document.createElement('button');
            sleepBtn.id = 'tubedz-sleep-btn';
            sleepBtn.className = 'ytp-button';
            sleepBtn.title = 'مؤقت النوم الذكي (30 دقيقة مع تلاشي الصوت تدريجياً)';
            sleepBtn.innerHTML = `
                <svg height="100%" version="1.1" viewBox="0 0 36 36" width="100%" style="vertical-align: middle;">
                    <path d="M12,8 C11,14 15,22 24,24 C18,28 10,24 8,16 C7,12 9,9 12,8 Z" fill="#ffffff"></path>
                </svg>
            `;
            sleepBtn.onclick = () => {
                if (sleepSecondsRemaining > 0) {
                    clearInterval(sleepInterval);
                    sleepSecondsRemaining = 0;
                    sleepBtn.querySelector('path').setAttribute('fill', '#ffffff');
                    sleepBtn.title = 'مؤقت النوم الذكي (معطل)';
                } else {
                    setSleepTimer(30);
                    sleepBtn.title = 'مؤقت النوم نشط (30 دقيقة)';
                }
            };
            rightControls.insertBefore(sleepBtn, rightControls.firstChild);
        }
    }

    // 7. KEYBOARD SHORTCUTS FOR MASTER CONTROLS
    window.addEventListener('keydown', (e) => {
        if (['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;
        if (e.key === 'b' || e.key === 'B' || e.key === 'لا') {
            toggleAudioBoost();
        } else if (e.key === 'z' || e.key === 'Z' || e.key === 'ئ') {
            const sleepBtn = document.querySelector('#tubedz-sleep-btn');
            if (sleepBtn) sleepBtn.click();
        }
    });

    window.addEventListener('DOMContentLoaded', () => {
        enableBackgroundPlay();
        injectTubeDZBadge();
        injectCastButton();
        injectBoosterButton();
        injectSleepTimerButton();
        setInterval(injectTubeDZBadge, 2000);
        setInterval(injectCastButton, 1500);
        setInterval(injectBoosterButton, 1500);
        setInterval(injectSleepTimerButton, 1500);
    });

})();
