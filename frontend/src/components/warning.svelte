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
        margin: 5%;
        height: fit-content;
        border-radius: 10px;
        background: var(--ternary);
        opacity: 1;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        flex-direction: row;
        gap: 10px;
        color: #333;
        padding: 1%;

        position: fixed;
        top: 0;
        right: 0;
        z-index: 3;
        width: 40%;
    }

    .symbol {
        font-size: 32px;
    }
</style>
