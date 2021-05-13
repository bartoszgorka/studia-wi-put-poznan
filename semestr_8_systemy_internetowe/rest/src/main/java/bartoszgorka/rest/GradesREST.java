package bartoszgorka.rest;

import bartoszgorka.models.Grade;
import bartoszgorka.storage.DB;

import javax.annotation.security.PermitAll;
import javax.annotation.security.RolesAllowed;
import javax.ws.rs.*;
import javax.ws.rs.core.*;
import java.util.Set;

@Path("/students/{index}/grades")
public class GradesREST {
    @GET
    @Produces({MediaType.APPLICATION_JSON, MediaType.APPLICATION_XML})
    @PermitAll
    public Set<Grade> getAllGradesForStudent(@PathParam("index") int index) {
        for (Grade g : DB.getGrades(index)) {
            g.clearLinks();
        }
        return DB.getGrades(index);
    }

    @POST
    @Consumes({MediaType.APPLICATION_JSON, MediaType.APPLICATION_XML})
    @Produces({MediaType.APPLICATION_JSON, MediaType.APPLICATION_XML})
    @RolesAllowed({"supervisor", "admin"})
    public Response registerNewGrade(@PathParam("index") int index, Grade rawGradeBody, @Context UriInfo uriInfo) throws NotFoundException, BadRequestException {
        Grade newGrade = DB.registerNewGrade(index, rawGradeBody);
        newGrade.clearLinks();

        UriBuilder builder = uriInfo.getAbsolutePathBuilder();
        builder.path(Integer.toString(newGrade.getID()));
        return Response.created(builder.build()).entity(newGrade).build();
    }
}