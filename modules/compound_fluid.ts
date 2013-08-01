class CompoundFluid {
    public names_: string[];
    public percents_: number[];
    public size_: number;

    public name: string;

    constructor() {
        this.size_ = 0;
        this.names_ = [];
        this.percents_ = [];
        this.name = "Anonymous";
    }

    public addSimpleFluid(name: string, percent: number = 0): void {
        this.size_ += 1;
        this.names_.push(name);
        this.percents_.push(percent);
    }

    public empty(): bool {
        return this.size_ == 0;
    }
}

class FluidVisualizer {
    private cf_: CompoundFluid;

    constructor(private div: HTMLElement) {
        this.cf_ = new CompoundFluid();
    }

    public addSF(name: string, percent: number): void  {
        this.cf_.addSimpleFluid(name, percent);
    }

    public draw(): void {
        var ih: string = "<div class='cf'>";
        ih += this.name2HTML();
        if (!this.cf_.empty()) ih += this.parts2HTML();
        ih += "</div>";

        this.div.innerHTML = ih;
    }

    private name2HTML(): string {
        return "<div class='cf_name'><p class='cf_name'>"
        + this.cf_.name + "</p></div>";
    }

    private parts2HTML(): string {
        var result: string = "<div class='cf_parts'><table class='cf_parts'>";

        var size: number = this.cf_.size_;
        var names: string[] = this.cf_.names_;
        var percents: number[] = this.cf_.percents_;

        for (var i = 0; i < size; i++) {
            result += "<tr>";
            result += "<td>" + names[i] + "</td>";
            result += "<td>" + percents[i] + "</td>";
            result += "</tr>";
        }

        result += "</table></div>";

        return result;
    }
 }

var FV = new FluidVisualizer(document.getElementById("container"));



