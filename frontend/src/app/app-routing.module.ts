import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AsymetricUnityTemplateComponent } from './asymetric-unity-template/asymetric-unity-template.component';

const routes: Routes = [
  { path: 'frontend/:variable', component: AsymetricUnityTemplateComponent },
  // Autres routes si nécessaire
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
