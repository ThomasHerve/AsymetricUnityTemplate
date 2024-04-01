import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { UrlService } from '../url.service';

@Component({
  selector: 'app-asymetric-unity-template',
  templateUrl: './asymetric-unity-template.component.html',
  styleUrls: ['./asymetric-unity-template.component.css']
})
export class AsymetricUnityTemplateComponent implements OnInit {

  value: string | undefined;
  variable: string | undefined;

  constructor(private route: ActivatedRoute, private urlService: UrlService) {
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.variable = params['variable'];
    });
  }

  onInputChange(event: Event) {
    // Accéder à la valeur du champ de texte à partir de l'événement
    this.value = (event.target as HTMLInputElement).value;
  }

  click() {
    this.urlService.publish(this.variable, this.value).subscribe((x)=>console.log)
  }
}
