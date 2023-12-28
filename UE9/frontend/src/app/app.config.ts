import {ApplicationConfig, importProvidersFrom} from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import {provideHttpClient, withInterceptorsFromDi} from "@angular/common/http";
import { provideAnimations } from '@angular/platform-browser/animations';
import {StarRatingConfig, StarRatingConfigService, StarRatingModule} from "angular-star-rating";
import { JwtModule} from "@auth0/angular-jwt";

export function tokenGetter() {
  return localStorage.getItem("access_token");
}


export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient(withInterceptorsFromDi()),
    provideAnimations(),
    StarRatingConfigService,
    importProvidersFrom(
      JwtModule.forRoot({
        config: {
          tokenGetter: tokenGetter,
          allowedDomains: ['localhost:8000']
        }
      })
    )
],
};
