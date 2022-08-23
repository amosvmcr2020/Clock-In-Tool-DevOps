<div class="warning-container">
    <div class="warn warning" />
    <slot />
</div>

<style>
    .warning-container {
        width: 90%;
        margin: 5%;
        height: 70px;
        border-radius: 10px;
        background: var(--ternary);
        opacity: 0.75;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        flex-direction: row;
        gap: 10px;
    }

    .warn,
    .warn::before,
    .warn::after {
        position: relative;
    }

    .warn {
        font-size: 36px;
        color: transparent;
        transform: translateY(-5px);
        margin-left: 10px;
    }

    .warn.warning {
        display: inline-block;

        top: 0.225em;

        width: 1.15em;
        height: 1.15em;

        overflow: hidden;
        border: none;
        background-color: transparent;
        border-radius: 0.625em;
    }

    .warn.warning::before {
        content: "";
        display: block;
        top: -0.08em;
        left: 0em;
        position: absolute;
        border: transparent 0.6em solid;
        border-bottom-color: orange;
        border-bottom-width: 1em;
        border-top-width: 0;
        box-shadow: #999 0 1px 1px;
    }

    .warn.warning::after {
        display: block;
        position: absolute;
        top: 0.3em;
        left: 0;
        width: 100%;
        padding: 0 1px;
        text-align: center;
        font-family: "Garamond";
        content: "!";
        font-size: 0.65em;
        font-weight: bold;
        color: #333;
    }
</style>
