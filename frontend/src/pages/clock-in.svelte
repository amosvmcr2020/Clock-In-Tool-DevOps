<script>
    import Clock from "../components/clock.svelte";
    import Warning from "../components/warning.svelte";
    let response = [];
</script>

<div class="page">
    <div class="page-title">Log your time</div>

    <!-- <div class="container-title">Clock in/out</div> -->
    <div class="clock-container">
        <Clock bind:response type="in" />
        <Clock bind:response type="out" />
    </div>
    {#if response[0] == "Error"}
        <div class="warning-container">
            <Warning>{response[1]}</Warning>
        </div>
    {:else if response[0] == "Success"}
        <div style="color: --text;">
            <!-- TODO: Add a success component -->
            {response[1]}
        </div>
    {/if}
</div>

<style>
    .clock-container {
        margin-top: 30px;
        display: flex;
        flex-direction: row;
        gap: 200px;
        justify-content: center;
    }
    .warning-container {
        color: #333;
    }
</style>
