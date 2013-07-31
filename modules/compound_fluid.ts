class FluidVisualizer {
    private words_: string[];
    private size_: number;

    constructor(private div: HTMLElement) {
        this.size_ = 0;
        this.words_ = [];
    }

    add(word: string): void  {
        this.words_.push(word);
        this.size_ += 1;
        this.redraw();
    }

    redraw(): void {
        this.div.innerHTML = "";
        for (var i = 0; i < this.size_; i++) {
            this.div.innerHTML += "<p>" + this.words_[i] + "</p>";
        }
    }
 }

var FV = new FluidVisualizer(document.getElementById("container"));



