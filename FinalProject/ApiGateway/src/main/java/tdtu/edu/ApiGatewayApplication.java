package tdtu.edu;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.function.RouterFunction;
import org.springframework.web.servlet.function.ServerRequest;
import org.springframework.web.servlet.function.ServerResponse;

import java.time.ZonedDateTime;
import java.util.function.BiFunction;

import static org.springframework.cloud.gateway.server.mvc.filter.FilterFunctions.addRequestHeader;
import static org.springframework.cloud.gateway.server.mvc.handler.GatewayRouterFunctions.route;
import static org.springframework.cloud.gateway.server.mvc.handler.HandlerFunctions.http;
import static org.springframework.cloud.gateway.server.mvc.predicate.GatewayRequestPredicates.after;
import static org.springframework.web.reactive.function.server.RequestPredicates.GET;


@SpringBootApplication
@EnableDiscoveryClient
@Configuration
public class ApiGatewayApplication {

	public static void main(String[] args) {
		SpringApplication.run(ApiGatewayApplication.class, args);
	}

//	@Bean
//	public RouterFunction<ServerResponse> routeConfig() {
//		return route("route_id")
//				.route(after(ZonedDateTime.parse("2023-12-06T19:03:47.789-05:00[America/New_York]")), http("http://example.com"))
//				.after((BiFunction<ServerRequest, ServerResponse, ServerResponse>) addRequestHeader("X-Trace-Token", "cd855f1a-0df3-4199-bc33-821dc797fc29"))
//				.build();
//	}

}
