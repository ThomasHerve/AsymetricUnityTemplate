import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { UrlService } from '../url.service';
import { interval } from 'rxjs';

@Component({
  selector: 'app-asymetric-unity-template',
  templateUrl: './asymetric-unity-template.component.html',
  styleUrls: ['./asymetric-unity-template.component.css']
})
export class AsymetricUnityTemplateComponent implements OnInit {

  variable: string | undefined;
  cooldown: number = 5;
  currentCooldown: number = 5;

  constructor(private route: ActivatedRoute, private urlService: UrlService) {
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.variable = params['variable'];
    });
    this.animation("0");
    this.animation("1");
    this.animation("2");
    this.animation("3");

    // Cooldown
    interval(100)
    .subscribe(() => {
      if(this.currentCooldown < this.cooldown) {
        this.currentCooldown += 0.1;
        if(this.currentCooldown > this.cooldown) {
          this.currentCooldown = this.cooldown;
          document.getElementById("0")!.style.backgroundColor = "#1a237e"
          document.getElementById("1")!.style.backgroundColor = "#1a237e"
          document.getElementById("2")!.style.backgroundColor = "#1a237e"
          document.getElementById("3")!.style.backgroundColor = "#1a237e"
          document.getElementById("0")!.style.filter = "grayscale(0%)"
          document.getElementById("1")!.style.filter = "grayscale(0%)"
          document.getElementById("2")!.style.filter = "grayscale(0%)"
          document.getElementById("3")!.style.filter = "grayscale(0%)"
        }
      }
    });

  }

  animation(value: string) {
    const animated = document.getElementById(value);

    animated!.addEventListener("animationend", (x) => {
      if(x.animationName == "anim") {
        animated?.classList.remove('anim');
      }
      else {
        animated?.classList.remove('loading');
      }
    });
  }

  click(value: string) {
    if(this.currentCooldown == this.cooldown) {
      this.currentCooldown = 0;
      document.getElementById("0")!.style.backgroundColor = "grey"
      document.getElementById("1")!.style.backgroundColor = "grey"
      document.getElementById("2")!.style.backgroundColor = "grey"
      document.getElementById("3")!.style.backgroundColor = "grey"
      document.getElementById("0")!.style.filter = "grayscale(100%)"
      document.getElementById("1")!.style.filter = "grayscale(100%)"
      document.getElementById("2")!.style.filter = "grayscale(100%)"
      document.getElementById("3")!.style.filter = "grayscale(100%)"
      const animated = document.getElementById(value);
      animated?.classList.add('anim');
      this.urlService.publish(this.variable, value).subscribe((x)=>console.log)  

      document.getElementById("0")!.classList.add('loading')
      document.getElementById("1")!.classList.add('loading')
      document.getElementById("2")!.classList.add('loading')
      document.getElementById("3")!.classList.add('loading')      
    }
  }
}
