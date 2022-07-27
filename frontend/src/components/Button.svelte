<script>
    export let func;
</script>

<button on:click={() => func()}>
    <slot />
</button>

<style>
    button {
        background-color: rgba(255, 255, 255, 0);
        color: white;
        text-transform: uppercase;
        font-size: 20px;
        padding: 20px;
        margin: 0;
        border-color: rgb(65, 107, 155);
        border-width: 2px;
    }
    button:active {
        background-color: rgb(65, 107, 155);
    }
</style>
