<script>
    import Icon from "@iconify/svelte";
</script>

<div class="warning-container">
    <div class="symbol">
        <Icon class="symbol" icon="ant-design:warning-filled" />
    </div>
    <slot />
</div>

<style>
    .warning-container {
        margin: 1%;
        height: 20px;
        border-radius: 10px;
        background: var(--alt-danger);
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
        width: fit-content;
        max-width: 40%;
        animation: slide-in 5s ease-in forwards;
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
