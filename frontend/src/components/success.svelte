<script>
    import Icon from "@iconify/svelte";
</script>

<div class="warning-container">
    <div class="symbol">
        <Icon icon="ep:success-filled" />
    </div>
    <slot />
</div>

<style>
    .warning-container {
        margin: 1%;
        height: fit-content;
        border-radius: 10px;
        background: var(--alt-success);
        opacity: 1;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        flex-direction: row;
        gap: 10px;
        color: var(--text);
        padding: 1%;

        position: absolute;
        right: 0;
        z-index: 99;
        width: 40%;
        animation: slide-in 4s ease-in forwards;
    }

    .symbol {
        font-size: 32px;
    }

    @keyframes slide-in {
        0% {
            right: -50%;
        }
        20% {
            right: 0%;
        }
        40% {
            right: 0;
        }
        60% {
            right: 0;
        }
        80% {
            right: 0;
        }
        100% {
            right: -50%;
        }
    }
</style>
